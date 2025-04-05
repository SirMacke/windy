const fs = require('fs');
const child_process = require('child_process');

class AM2320 {
  constructor(busNumber = 1, address = 0x5C) {
    this.busNumber = busNumber;
    this.address = address;
    this.devicePath = `/dev/i2c-${busNumber}`;
    this.fd = null;
  }

  open() {
    if (this.fd) return;
    
    try {
      // Set I2C slave address using i2cset command
      child_process.execSync(`i2cset -y ${this.busNumber} ${this.address} 0x00 b`);
      
      // Open the device file
      this.fd = fs.openSync(this.devicePath, 'r+');
      console.log(`Connected to AM2320 on ${this.devicePath} at address 0x${this.address.toString(16)}`);
    } catch (err) {
      console.error(`Error setting up I2C: ${err.message}`);
      throw new Error(`Failed to open I2C device: ${err.message}`);
    }
  }

  close() {
    if (this.fd !== null) {
      fs.closeSync(this.fd);
      this.fd = null;
    }
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Calculate CRC16 (Modbus)
  _calculateCRC16(buffer) {
    let crc = 0xFFFF;
    
    for (let i = 0; i < buffer.length; i++) {
      crc ^= buffer[i];
      
      for (let j = 0; j < 8; j++) {
        if (crc & 0x0001) {
          crc >>= 1;
          crc ^= 0xA001;
        } else {
          crc >>= 1;
        }
      }
    }
    
    return crc;
  }

  async read() {
    // Using i2c-tools commands instead of direct file operations
    try {
      // Wake up the sensor (write to address without sending data)
      child_process.execSync(`i2cset -y ${this.busNumber} ${this.address} 0x00 b`);
      
      // Wait for sensor to wake up
      await this._sleep(10);
      
      // Send the read command: function code 0x03, start address 0x00, read 4 bytes
      child_process.execSync(
        `i2cset -y ${this.busNumber} ${this.address} 0x03 0x00 0x04 i`
      );
      
      // Wait for the sensor to process
      await this._sleep(2);
      
      // Read 8 bytes from the device (includes function code, length, data, and CRC)
      const output = child_process.execSync(
        `i2cget -y ${this.busNumber} ${this.address} 0x00 i 8`
      ).toString().trim();
      
      // Parse the output (format will be like "0x03041234ABCD")
      const hexData = output.replace('0x', '');
      const bytes = [];
      
      for (let i = 0; i < hexData.length; i += 2) {
        bytes.push(parseInt(hexData.substr(i, 2), 16));
      }
      
      // Check function code
      if (bytes[0] !== 0x03) {
        throw new Error(`Invalid function code: ${bytes[0]}`);
      }
      
      // Check data length
      if (bytes[1] !== 0x04) {
        throw new Error(`Invalid data length: ${bytes[1]}`);
      }
      
      // Extract data
      const humidityHigh = bytes[2];
      const humidityLow = bytes[3];
      const temperatureHigh = bytes[4];
      const temperatureLow = bytes[5];
      
      // Calculate CRC
      const crc = (bytes[7] << 8) | bytes[6];
      const calculatedCRC = this._calculateCRC16(Buffer.from(bytes.slice(0, 6)));
      
      if (crc !== calculatedCRC) {
        throw new Error(`CRC check failed: ${crc} !== ${calculatedCRC}`);
      }
      
      // Calculate actual values
      const humidity = ((humidityHigh << 8) | humidityLow) / 10.0;
      const temperature = ((temperatureHigh << 8) | temperatureLow) / 10.0;
      
      return { temperature, humidity };
      
    } catch (err) {
      throw new Error(`Error reading sensor: ${err.message}`);
    }
  }
}

module.exports = AM2320;