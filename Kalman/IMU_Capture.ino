// XIAO BLE Sense LSM6DS3 Accelerometer Raw Data 

#include "LSM6DS3.h"
#include "Wire.h"
#include "kalman.h"
//Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);  //I2C device address 0x6A

#define CONVERT_G_TO_MS2 9.80665f
#define FREQUENCY_HZ 50.0f
#define CUTOFF_FREQUENCY 20
#define INTERVAL_MS (1000 / (FREQUENCY_HZ + 1))
#define SAMPLING_PERIOD (1/FREQUENCY_HZ)

static unsigned long last_interval_ms = 0;
float rollEstimate_rad;
float pitchEstimate_rad;
float rollAcc_rad  = 0.0f;
float pitchAcc_rad = 0.0f;
float rollGyr_rad = 0.0f;
float pitchGyr_rad = 0.0f;
float P_init[2] = {0.1f, 0.1f};
float Q[2] = {0.001f, 0.001f};
float R[3] = {0.03f, 0.011f, 0.011f};
double acc_rdg[3],gyr_rdg[3]; //0 is x, 1 is y, 2 is z
double offset[6]={0.051,0.1042,-0.1294,-0.6362,-0.6586,0.9682};
double alpha;
int count=0;
float yaw = 0;
EKF ekf;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  if (myIMU.begin() != 0) {
    Serial.println("Device error");
  } else {
    Serial.println("Device OK!");
    EKF_Init(&ekf, P_init, Q, R);
    double timeConstant = 1 / (2 * PI * CUTOFF_FREQUENCY);
    alpha = timeConstant / (timeConstant + SAMPLING_PERIOD);
    rollEstimate_rad  = 0.0f;
    pitchEstimate_rad = 0.0f;
    for(int i=0;i<3;i++){
      acc_rdg[i]=0;
      gyr_rdg[i]=0;
    }
  }
}



void loop() {
  if (millis() > last_interval_ms + INTERVAL_MS) {
    last_interval_ms = millis();
    acc_rdg[1]= alpha * acc_rdg[1]  + (1 - alpha) * (myIMU.readFloatAccelX() * CONVERT_G_TO_MS2 + offset[1]);
    acc_rdg[0]= alpha * acc_rdg[0]  + (1 - alpha) * (myIMU.readFloatAccelY() * CONVERT_G_TO_MS2 + offset[0]);
    acc_rdg[2]= alpha * acc_rdg[2]  - (1 - alpha) * (myIMU.readFloatAccelZ() * CONVERT_G_TO_MS2 + offset[2]);
    gyr_rdg[1]= alpha * gyr_rdg[1]  + (1 - alpha) * (myIMU.readFloatGyroX()  + offset[4]);
    gyr_rdg[0]= alpha * gyr_rdg[0]  + (1 - alpha) * (myIMU.readFloatGyroY()  + offset[3]);
    gyr_rdg[2]= alpha * gyr_rdg[2]  - (1 - alpha) * (myIMU.readFloatGyroZ()  + offset[5]);
    EKF_Predict(&ekf, gyr_rdg[0], gyr_rdg[1], gyr_rdg[2], SAMPLING_PERIOD);
    if(count>=5){
      EKF_Update(&ekf, acc_rdg[0], acc_rdg[1], acc_rdg[2]);
      count=0;
    }else{
      count++;
    }
    Serial.print(ekf.phi_r * RAD_TO_DEG, 4);
    Serial.print('\t');
    Serial.print(ekf.theta_r * RAD_TO_DEG, 4);
    Serial.print('\t');
    Serial.println(yaw, 4);
  }
}

