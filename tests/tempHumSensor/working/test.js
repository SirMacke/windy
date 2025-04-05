const { execSync } = require('child_process');

const SENSOR_ADDR = '0x5c';

// Wake up sensor
console.log('Waking up sensor...');
try {
    execSync(`i2cset -y 1 ${SENSOR_ADDR} 0x00 c`);
} catch (err) {
    console.log('Error waking up sensor:', err);
}
sleep(1);

// Send read command
console.log('Sending read command...');
execSync(`i2cset -y 1 ${SENSOR_ADDR} 0x03 0x00 0x04 i`);
sleep(2);

// Read 8 bytes from sensor
console.log('Reading sensor data...');
const output = execSync(`i2cget -y 1 ${SENSOR_ADDR} 0x00 i 8`).toString().trim();
console.log('Raw data:', output);
// Ex: 0x03 0x04 0x00 0xc7 0x01 0x20 0x40 0x5d

const bytes = output.split(' ').map(hex => parseInt(hex, 16));

const functionCode = bytes[0];
const dataLen = bytes[1];

// Combine two bytes into a 16-bit humidity value
// bytes[2] is shifted left 8 bits (multiplied by 256) and added to bytes[3]
// This reconstructs the original 16-bit humidity reading from the sensor
const humidityRaw = (bytes[2] << 8) + bytes[3];
const temperatureRaw = (bytes[4] << 8) + bytes[5];

const humidity = (humidityRaw / 10).toFixed(1);
const temperature = (temperatureRaw / 10).toFixed(1);

console.log(`Temperature: ${temperature}°C`);
console.log(`Humidity: ${humidity}%`);

function sleep(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}