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

function handleCharacteristicValueChanged(event) {
  const value = event.target.value;
  console.log('Received ' + value);
}