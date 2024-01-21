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
  // console.log(`${ax.toFixed(4)} ${ay.toFixed(4)} ${az.toFixed(4)} ${gx.toFixed(4)} ${gy.toFixed(4)} ${gz.toFixed(4)}`);
  
}


function App() {
  async function sendDataToBackend() {
    let body = JSON.stringify({ readings });
    
    console.log(body);
    //response has the format "{'prediction': 'A'}" where A is the predicted letter in the alphabet
    fetch('http://localhost:8035/capstone/api/predictions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
  
      },
      body: body
    })
      .then(response => response.json())
      .then(data => {
        setPrediction(data.prediction);
      })
      .catch(error => {
        console.error('Error sending data to backend:', error);
      });
  }
  const [buttonClicked, setButtonClicked] = useState(false);
  const buttonText= 'Start Recording';
  const [prediction, setPrediction] = useState('idle');
  const handleButtonClick = () => {
    setButtonClicked(true);
    connectBluetooth();
  };
  const handleRecording = () => {
    readings = [];
    //set text count down from 2 to 1 for preparation
    //call sendtoBackend after 2 seconds
    setTimeout(sendDataToBackend, 2000);
  }
  return (
    <div>
      {!buttonClicked && <button onClick={handleButtonClick}>Connect to your device</button>}
      <button onClick={handleRecording}>{buttonText}</button>
      {buttonClicked && <p>Prediction: {prediction}</p>}
    </div>
  );
}

export default App;
