const fs = require('fs');
const path = require('path');

class AM2320 {
  constructor(busNumber = 1, address = 0x5C) {
    this.devicePath = `/dev/i2c-${busNumber}`;
    this.address = address;
    this.fd = null;
  }

  open() {
    if (this.fd) return;
    try {
      this.fd = fs.openSync(this.devicePath, 'r+');
      // Set the I2C slave address
      this._ioctl(0x0703, this.address);
      console.log(`Connected to AM2320 on ${this.devicePath} at address 0x${this.address.toString(16)}`);
    } catch (err) {
      throw new Error(`Failed to open I2C device: ${err.message}`);
    }
  }

  close() {
    if (this.fd !== null) {
      fs.closeSync(this.fd);
      this.fd = null;
    }
  }

  _ioctl(cmd, arg) {
    // This requires the native ioctl binding
    const { ioctl } = require('./ioctl_native.cc');
    return ioctl(this.fd, cmd, arg);
  }

  _writeBytes(bytes) {
    return fs.writeSync(this.fd, Buffer.from(bytes));
  }

  _readBytes(length) {
    const buffer = Buffer.alloc(length);
    fs.readSync(this.fd, buffer, 0, length, null);
    return buffer;
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
    this.open();

    // Wake up the sensor (AM2320 requires this)
    try {
      this._writeBytes([0x00]);
    } catch (e) {
      // Expected to fail with EREMOTEIO, it's just to wake up the device
    }
    
    // Wait for sensor to wake up
    await this._sleep(10);
    
    // Send the read command - function code 0x03, start address 0x00, read 4 bytes
    this._writeBytes([0x03, 0x00, 0x04]);
    
    // Wait for the sensor to process
    await this._sleep(2);
    
    // Read the response (3 bytes of header + 4 bytes of data + 2 bytes of CRC)
    const response = this._readBytes(8);
    
    // Check function code
    if (response[0] !== 0x03) {
      throw new Error(`Invalid function code: ${response[0]}`);
    }
    
    // Check data length
    if (response[1] !== 0x04) {
      throw new Error(`Invalid data length: ${response[1]}`);
    }
    
    // Extract data
    const humidityHigh = response[2];
    const humidityLow = response[3];
    const temperatureHigh = response[4];
    const temperatureLow = response[5];
    
    // Calculate CRC
    const crc = (response[7] << 8) | response[6];
    const calculatedCRC = this._calculateCRC16(response.slice(0, 6));
    
    if (crc !== calculatedCRC) {
      throw new Error(`CRC check failed: ${crc} !== ${calculatedCRC}`);
    }
    
    // Calculate actual values
    const humidity = ((humidityHigh << 8) | humidityLow) / 10.0;
    const temperature = ((temperatureHigh << 8) | temperatureLow) / 10.0;
    
    return { temperature, humidity };
  }
}

// Export the AM2320 class
module.exports = AM2320;