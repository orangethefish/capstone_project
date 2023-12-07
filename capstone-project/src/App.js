import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";

let readings = [];


function connectBluetooth() {
  navigator.bluetooth.requestDevice({ filters: [{ services: [0x1101] }] })
.then(device => device.gatt.connect())
.then(server => server.getPrimaryService('00001101-0000-1000-8000-00805f9b34fb'))
.then(service => service.getCharacteristic('00002101-0000-1000-8000-00805f9b34fb'))
.then(characteristic => characteristic.startNotifications())
.then(characteristic => {
  characteristic.addEventListener('characteristicvaluechanged',
                                  handleCharacteristicValueChanged);
  setInterval(() => {
    sendDataToBackend();
  }, 2000);
  console.log('Notifications have been started.');
})
.catch(error => { console.error(error); });
}

function handleCharacteristicValueChanged(event) {
  const value = event.target.value;
  const data = new Uint8Array(value.buffer);
  const ax = new DataView(data.buffer, 0).getFloat32(0, true);
  const ay = new DataView(data.buffer, 4).getFloat32(0, true);
  const az = new DataView(data.buffer, 8).getFloat32(0, true);
  const gx = new DataView(data.buffer, 12).getFloat32(0, true);
  const gy = new DataView(data.buffer, 16).getFloat32(0, true);
  const gz = new DataView(data.buffer, 20).getFloat32(0, true);
  readings.push({ ax, ay, az, gx, gy, gz });
  // console.log(`Acc: ${ax.toFixed(4)} ${ay.toFixed(4)} ${az.toFixed(4)}`);
  
}

async function sendDataToBackend() {
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
  let body = JSON.stringify({ readings });
  console.log(body);
  // Clear the arrays for the next set of data
  readings = [];
}

function App() {
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
