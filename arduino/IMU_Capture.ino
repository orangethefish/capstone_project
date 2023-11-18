// XIAO BLE Sense LSM6DS3 Accelerometer Raw Data 

#include <ArduinoBLE.h>
#include "LSM6DS3.h"

// BLE UUIDs

#define BLE_UUID_IMU_SERVICE              "1101"
#define BLE_UUID_ACC_CHAR                 "2101"
#define BLE_UUID_GYRO_CHAR                "2102"
#define BLE_DEVICE_NAME                           "IMU_Sensor"
#define BLE_LOCAL_NAME                            "IMU_Sensor"
// Define Sensors
double acc_rdg[3],gyr_rdg[3]; //0 is x, 1 is y, 2 is z
#define ACC_SENSOR_UPDATE_INTERVAL                (20)
#define GYRO_SENSOR_UPDATE_INTERVAL               (20)

union sensor_data{
  struct __attribute__((packed)) {
    float values[3]; // float array for data (it holds 3)
    bool updated = false;
  };
  uint8_t bytes[3 * sizeof(float)]; // size as byte array 
};

union sensor_data accData;
union sensor_data gyroData;
BLEService IMUService(BLE_UUID_IMU_SERVICE);
BLECharacteristic accCharacteristic(BLE_UUID_ACC_CHAR, BLERead | BLENotify, sizeof accData.bytes);
BLECharacteristic gyroCharacteristic(BLE_UUID_GYRO_CHAR, BLERead | BLENotify, sizeof gyroData.bytes);

//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);  //I2C device address 0x6A

#define CONVERT_G_TO_MS2 9.80665f
#define FREQUENCY_HZ 50.0f
#define CUTOFF_FREQUENCY 20
#define INTERVAL_MS (1000 / (FREQUENCY_HZ + 1))
#define SAMPLING_PERIOD (1/FREQUENCY_HZ)
static unsigned long last_interval_ms = 0;

double offset[6]={0.051,0.1042,-0.1294,-0.6362,-0.6586,0.9682};
double alpha;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  if (myIMU.begin() != 0) {
    Serial.println("Device error");
  } else {
    Serial.println("Device OK!");
    alpha = 1 / (2 * PI * CUTOFF_FREQUENCY * SAMPLING_PERIOD);
    for(int i=0;i<3;i++){
      acc_rdg[i]=0;
      gyr_rdg[i]=0;
    }
  }
  if (!setupBleMode()) {
    while (1);
  } else {
    Serial.println("BLE initialized. Waiting for clients to connect.");
  }
  for (int i = 0; i < 3; i++) {
    accData.values[i] = 0;
    gyroData.values[i] = 0;
  }
}



void loop() {
  bleTask();
  if (accSensorTask()) {
    // accPrintTask();
  }
  if (gyroSensorTask()){
    // gyroPrintTask();
  }
  if (millis() > last_interval_ms + INTERVAL_MS) {
    last_interval_ms = millis();
    acc_rdg[1]= alpha * acc_rdg[1]  + (1 - alpha) * (myIMU.readFloatAccelX() * CONVERT_G_TO_MS2 + offset[1]);
    acc_rdg[0]= alpha * acc_rdg[0]  + (1 - alpha) * (myIMU.readFloatAccelY() * CONVERT_G_TO_MS2 + offset[0]);
    acc_rdg[2]= alpha * acc_rdg[2]  - (1 - alpha) * (myIMU.readFloatAccelZ() * CONVERT_G_TO_MS2 + offset[2]);
    gyr_rdg[1]= alpha * gyr_rdg[1]  + (1 - alpha) * (myIMU.readFloatGyroX()  + offset[4]);
    gyr_rdg[0]= alpha * gyr_rdg[0]  + (1 - alpha) * (myIMU.readFloatGyroY()  + offset[3]);
    gyr_rdg[2]= alpha * gyr_rdg[2]  - (1 - alpha) * (myIMU.readFloatGyroZ()  + offset[5]);
    Serial.print(acc_rdg[0], 4);
    Serial.print('\t');
    Serial.print(acc_rdg[1], 4);
    Serial.print('\t');
    Serial.print(acc_rdg[2], 4);
    Serial.print('\t');
    Serial.print(gyr_rdg[0], 4);
    Serial.print('\t');
    Serial.print(gyr_rdg[1], 4);
    Serial.print('\t');
    Serial.println(gyr_rdg[2], 4);
  }
}

/*-----------------------------------------------------------------------------------*/

bool accSensorTask() {
  static long previousMillis2 = 0;
  unsigned long currentMillis2 = millis();
  if (currentMillis2 - previousMillis2 < ACC_SENSOR_UPDATE_INTERVAL) {
    return false;
  }
  previousMillis2 = currentMillis2;
  accData.values[0] = acc_rdg[0]; // 0.11
  accData.values[1] = acc_rdg[1]; // 1.13
  accData.values[2] = acc_rdg[2]; // -1.13
  accData.updated = true;
  return accData.updated;
}

bool gyroSensorTask() {
  static long previousMillis2 = 0;
  unsigned long currentMillis2 = millis();
  static float x = 0.00, y = 0.00, z = 0.00;
  if (currentMillis2 - previousMillis2 < GYRO_SENSOR_UPDATE_INTERVAL) {
    return false;
  }
  previousMillis2 = currentMillis2;
  gyroData.values[0] = gyr_rdg[0]; // 0.11
  gyroData.values[1] = gyr_rdg[1]; // 1.13
  gyroData.values[2] = gyr_rdg[2]; // -1.13
  gyroData.updated = true;
  return gyroData.updated;
}

/*-----------------------------------------------------------------------------------*/
bool setupBleMode() {
  if (!BLE.begin()) {
    return false;
  }

  // set advertised local name and service UUID:
  BLE.setDeviceName(BLE_DEVICE_NAME);
  BLE.setLocalName(BLE_LOCAL_NAME);
  BLE.setAdvertisedService(IMUService);

  // BLE add characteristics
  IMUService.addCharacteristic(accCharacteristic);
  IMUService.addCharacteristic(gyroCharacteristic);

  // add service
  BLE.addService(IMUService);

  // set the initial value for the characteristic:
  accCharacteristic.writeValue(accData.bytes, sizeof accData.bytes);
  gyroCharacteristic.writeValue(gyroData.bytes, sizeof gyroData.bytes);

  // set BLE event handlers
  BLE.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  BLE.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  // start advertising
  BLE.advertise();

  return true;
}

void bleTask()
{
  const uint32_t BLE_UPDATE_INTERVAL = 10;
  static uint32_t previousMillis = 0;
  uint32_t currentMillis = millis();
  if (currentMillis - previousMillis >= BLE_UPDATE_INTERVAL) {
    previousMillis = currentMillis;
    BLE.poll();
  }
  if (accData.updated) {
    // Bluetooth does not define accelerometer
    // Units in G
    int16_t accelerometer_X = round(accData.values[0] * 100.0);
    int16_t accelerometer_Y = round(accData.values[1] * 100.0);
    int16_t accelerometer_Z = round(accData.values[2] * 100.0);
    accCharacteristic.writeValue(accData.bytes, sizeof accData.bytes);
    accData.updated = false;
  }

  if (gyroData.updated) {
    // Bluetooth does not define gyroscope
    // Units in dps
    int16_t gyro_X = round(gyroData.values[0] * 100.0);
    int16_t gyro_Y = round(gyroData.values[1] * 100.0);
    int16_t gyro_Z = round(gyroData.values[2] * 100.0);
    gyroCharacteristic.writeValue(gyroData.bytes, sizeof gyroData.bytes);
    gyroData.updated = false;
  }
}
/*-----------------------------------------------------------------------------------*/

void accPrintTask() {
  Serial.print("AccX = ");
  Serial.print(accData.values[0]);
  Serial.println(" G");

  Serial.print("AccY = ");
  Serial.print(accData.values[1]);
  Serial.println(" G");

  Serial.print("AccZ = ");
  Serial.print(accData.values[2]);
  Serial.println(" G");

  Serial.print("Acc. Subscription Status: ");
  Serial.println(accCharacteristic.subscribed());
}

void gyroPrintTask() {
  Serial.print("gyroX = ");
  Serial.print(gyroData.values[0]);
  Serial.println(" dps");

  Serial.print("gyroY = ");
  Serial.print(gyroData.values[1]);
  Serial.println(" dps");

  Serial.print("gyroZ = ");
  Serial.print(gyroData.values[2]);
  Serial.println(" dps");

  Serial.print("Gyro. Subscription Status: ");
  Serial.println(gyroCharacteristic.subscribed());
}
/*-----------------------------------------------------------------------------------*/

void blePeripheralConnectHandler(BLEDevice central) {
  Serial.print(F( "Connected to central: " ));
  Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLEDevice central) {
  Serial.print(F("Disconnected from central: "));
  Serial.println(central.address());
}