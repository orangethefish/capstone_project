import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";

let accelerometer = [];
let gyroscope = [];

// Define a variable to track the elapsed time
let elapsedTime = 0;

function connectBluetooth() {
  navigator.bluetooth.requestDevice({ filters: [{ services: [0x1101] }] })
    .then(device => device.gatt.connect())
    .then(server => server.getPrimaryService('00001101-0000-1000-8000-00805f9b34fb'))
    .then(service => {
      const acc_rdg = service.getCharacteristic('00002101-0000-1000-8000-00805f9b34fb');
      const gyro_rdg = service.getCharacteristic('00002102-0000-1000-8000-00805f9b34fb');
      return Promise.all([acc_rdg, gyro_rdg]);
    })
    .then(characteristics => {
      const accCharacteristic = characteristics[0];
      const gyroCharacteristic = characteristics[1];
      
      accCharacteristic.startNotifications();
      accCharacteristic.addEventListener('characteristicvaluechanged', handleAccCharacteristicValueChanged);
      
      gyroCharacteristic.startNotifications();
      gyroCharacteristic.addEventListener('characteristicvaluechanged', handleGyroCharacteristicValueChanged);
      
      console.log('Notifications have been started.');

      setInterval(() => {
        elapsedTime += 1; // Increment the elapsed time by 2 seconds

        // Check if 2 seconds have passed
        if (elapsedTime >= 2) {
          sendDataToBackend();
          elapsedTime = 0; // Reset the elapsed time
        }
      }, 1000);
    })
    .catch(error => { console.error(error); });
}

function handleAccCharacteristicValueChanged(event) {
  const value = event.target.value;
  const data = new Uint8Array(value.buffer);
  const ax = new DataView(data.buffer, 0).getFloat32(0, true);
  const ay = new DataView(data.buffer, 4).getFloat32(0, true);
  const az = new DataView(data.buffer, 8).getFloat32(0, true);
  accelerometer.push({ ax, ay, az });
  // console.log(`Acc: ${ax.toFixed(4)} ${ay.toFixed(4)} ${az.toFixed(4)}`);
}

function handleGyroCharacteristicValueChanged(event) {
  const value = event.target.value;
  const data = new Uint8Array(value.buffer);
  const gx = new DataView(data.buffer, 0).getFloat32(0, true);
  const gy = new DataView(data.buffer, 4).getFloat32(0, true);
  const gz = new DataView(data.buffer, 8).getFloat32(0, true);
  gyroscope.push({ gx, gy, gz });
  // console.log(`Gyro: ${gx.toFixed(4)} ${gy.toFixed(4)} ${gz.toFixed(4)}`);
}

function sendDataToBackend() {
  // Send accelerometer and gyroscope data to the backend API
  // using fetch or any other HTTP library
  // fetch('backend-api-url', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json'
  //   },
  //   body: JSON.stringify({ accelerometer, gyroscope })
  // })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log('Data sent to backend:', data);
  //   })
  //   .catch(error => {
  //     console.error('Error sending data to backend:', error);
  //   });
  console.log(accelerometer);
  // console.log(gyroscope);
  // Clear the arrays for the next set of data
  accelerometer = [];
  gyroscope = [];
}

function App() {
  const [acc, setAcc] = useState('');
  const [gyro, setGyro] = useState('');
  const [buttonClicked, setButtonClicked] = useState(false);

  const handleButtonClick = () => {
    setButtonClicked(true);
    connectBluetooth();
  };

  return (
    <div>
      {!buttonClicked && <button onClick={handleButtonClick}>Connect to your device</button>}
    </div>
  );
}

export default App;
