const fs = require('fs');

const LED_PATH = '/sys/class/leds/ACT/brightness';

// Helper functions
const readLedState = () => {
  try {
    return parseInt(fs.readFileSync(LED_PATH, 'utf8').trim());
  } catch (error) {
    throw new Error(`Failed to read LED state: ${error.message}`);
  }
};

const writeLedState = (state) => {
  try {
    fs.writeFileSync(LED_PATH, state.toString());
    return true;
  } catch (error) {
    throw new Error(`Failed to write LED state: ${error.message}`);
  }
};

const getLedStatus = (state) => state >= 1 ? 'ON' : 'OFF';

// Main program
let initialState;
try {
  initialState = readLedState();
  console.log(`Initial LED state: ${getLedStatus(initialState)}`);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}

let currentState = 0;
console.log('Temporarily blinking ACT LED. Press Ctrl+C to exit.');

const interval = setInterval(() => {
  currentState = currentState ? 0 : 1;
  try {
    writeLedState(currentState);
    console.log(`LED: ${getLedStatus(currentState)}`);
  } catch (error) {
    console.error(error.message);
    clearInterval(interval);
    process.exit(1);
  }
}, 1000);

// Cleanup handler
process.on('SIGINT', () => {
  clearInterval(interval);
  try {
    writeLedState(initialState);
    console.log(`Restored LED to initial state: ${getLedStatus(initialState)}`);
  } catch (error) {
    console.error(error.message);
  }
  console.log('Exiting without modifying system control.');
  process.exit(0);
});