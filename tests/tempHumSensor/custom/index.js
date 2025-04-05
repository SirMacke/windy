const AM2320 = require('./am2320-simple');

async function main() {
  const sensor = new AM2320(1, 0x5C); // Bus 1, address 0x5C
  
  try {
    console.log('Reading AM2320 sensor...');
    const { temperature, humidity } = await sensor.read();
    
    console.log(`Temperature: ${temperature.toFixed(1)}°C`);
    console.log(`Humidity: ${humidity.toFixed(1)}%`);
  } catch (err) {
    console.error('Error reading sensor:', err.message);
  } finally {
    sensor.close();
  }
}

main();