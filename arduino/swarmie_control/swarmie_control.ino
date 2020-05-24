//////////////////////////
////Required Libraries////
//////////////////////////

//Built-in Arduino libraries
#include <Wire.h>

//Custom libraries located in Swarmathon-Arduino repo
#include <L3G.h>
#include <LPS.h>
#include <LSM303.h>
#include <Movement.h>
#include <NewPing.h>
#include <Odometry.h>
#include <Buzzer.h>

// Constants
#define PI 3.14159265358979323846
#define RAD2DEG(radianAngle) (radianAngle * 180.0 / PI)
#define DEG2RAD(degreeAngle) (degreeAngle * PI / 180.0)

////////////////
////Settings////
////////////////

//Movement (VNH5019 Motor Driver Carrier)
byte rightDirectionA = A3; //"clockwise" input
byte rightDirectionB = A2; //"counterclockwise" input
byte rightSpeedPin = 11; //PWM input
byte leftDirectionA = A5; //"clockwise" input
byte leftDirectionB = A4; //"counterclockwise" input
byte leftSpeedPin = 10; //PWM input

// Modify before merge

//Odometry (8400 CPR Encoder)
byte rightEncoderA = 7;
byte rightEncoderB = 8;
byte leftEncoderA = 0;
byte leftEncoderB = 1;
float wheelBase = 27.8; //distance between left and right wheels (in cm)
float wheelDiameter = 12.2; //diameter of wheel (in cm)
int cpr = 8400; //"cycles per revolution" -- number of encoder increments per one wheel revolution

//Serial (USB <--> Intel NUC)
String rxBuffer;
unsigned long watchdogTimer = 1000; //fail-safe in case of communication link failure (in ms)
unsigned long lastCommTime = 0; //time of last communication from NUC (in ms)

//Ultrasound (Ping))))
byte leftSideSignal = 9;
byte leftSignal = 4;
byte centerSignal = 5;
byte rightSignal = 6;
byte rightSideSignal = 12;

//Buzzer
byte buzzerPin = 13;


////////////////////////////
////Class Instantiations////
////////////////////////////

L3G gyroscope;
LSM303 magnetometer_accelerometer;
LPS pressure;
Movement move = Movement(rightSpeedPin, rightDirectionA, rightDirectionB, leftSpeedPin, leftDirectionA, leftDirectionB);
Odometry odom = Odometry(rightEncoderA, rightEncoderB, leftEncoderA, leftEncoderB, wheelBase, wheelDiameter, cpr);
NewPing leftSideUS(leftSideSignal, leftSideSignal, 330);
NewPing leftUS(leftSignal, leftSignal, 330);
NewPing centerUS(centerSignal, centerSignal, 330);
NewPing rightUS(rightSignal, rightSignal, 330);
NewPing rightSideUS(rightSideSignal, rightSideSignal, 330);
Buzzer buzz = Buzzer(buzzerPin);


/////////////
////Setup////
/////////////

void setup()
{
  Serial.begin(115200);
  while (!Serial) {} //wait for Serial to complete initialization before moving on

  Wire.begin();

  if (imuStatus()) {
    imuInit();
  }
  rxBuffer = "";
}


/////////////////
////Main Loop////
/////////////////

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == ',' || c == '\n') {
      parse();
      rxBuffer = "";
      lastCommTime = millis();
    }
    else if (c > 0) {
      rxBuffer += c;
    }
  }
  if (millis() - lastCommTime > watchdogTimer) {
    move.stop();
  }
}


////////////////////////
//Parse receive buffer//
////////////////////////

void parse() {
  if (rxBuffer == "v") {
    int speedL = Serial.parseInt();
    int speedR = Serial.parseInt();
    
    if (speedL >= 0 && speedR >= 0) {
      move.forward(speedL, speedR);
    }
    else if (speedL <= 0 && speedR <= 0) {
      move.backward(speedL*-1, speedR*-1);
    }
    else if (speedL <= 0 && speedR >= 0) {
      move.rotateLeft(speedL*-1, speedR);
    }
    else {
      move.rotateRight(speedL, speedR*-1);
    }
  }
  else if (rxBuffer == "s") {
    move.stop();
  }
  else if (rxBuffer == "b") {
    int state = Serial.parseInt();
    Serial.println(state);

    if(state == 0){
      buzz.arrived();
    }
    else if(state == 1){
      buzz.rotate();
    }
    else{
      buzz.error();
    }
  }
  else if (rxBuffer == "d") {
    Serial.print("IMU,");
    bool imuStatusFlag = imuStatus();
    Serial.print(String(imuStatusFlag) + ",");
    if (imuStatusFlag) {
      imuInit();
      Serial.println(updateIMU());
    }
    else {
      Serial.println(",,,,,,,,");
    }

    Serial.println("ODOM," + String(1) + "," + updateOdom());

    Serial.print("USL,");
    int leftUSValue = leftUS.ping_cm();
    Serial.print(String(leftUSValue > 0 ? 1 : 0) + ",");
    if (leftUSValue > 0) {
      Serial.println(String(leftUSValue));
    }
    else {
      Serial.println();
    }

    Serial.print("USC,");
    int centerUSValue = centerUS.ping_cm();
    Serial.print(String(centerUSValue > 0 ? 1 : 0) + ",");
    if (centerUSValue > 0) {
      Serial.println(String(centerUSValue));
    }
    else {
      Serial.println();
    }

    Serial.print("USR,");
    int rightUSValue = rightUS.ping_cm();
    Serial.print(String(rightUSValue > 0 ? 1 : 0) + ",");
    if (rightUSValue > 0) {
      Serial.println(String(rightUSValue));
    }
    else {
      Serial.println();
    }
    Serial.print("USSR,");
    int rightSideUSValue = rightSideUS.ping_cm();
    Serial.print(String(rightSideUSValue > 0 ? 1 : 0) + ",");
    if (rightSideUSValue > 0) {
      Serial.println(String(rightSideUSValue));
    }
    else {
      Serial.println();
    }
    Serial.print("USSL,");
    int leftSideUSValue = leftSideUS.ping_cm();
    Serial.print(String(leftSideUSValue > 0 ? 1 : 0) + ",");
    if (leftSideUSValue > 0) {
      Serial.println(String(leftSideUSValue));
    }
    else {
      Serial.println();
    }
  }
}


//////////////////////////
//Update transmit buffer//
//////////////////////////

String updateIMU() {
  //Update current sensor values
  gyroscope.read();
  magnetometer_accelerometer.read();

  if (!gyroscope.timeoutOccurred() && !magnetometer_accelerometer.timeoutOccurred()) {
    //Collect updated values
    LSM303::vector<int16_t> acc = magnetometer_accelerometer.a;
    L3G::vector<int16_t> gyro = gyroscope.g;
    LSM303::vector<int16_t> mag = magnetometer_accelerometer.m;

    //Convert accelerometer digits to milligravities, then to gravities, and finally to meters per second squared
    LSM303::vector<float> linear_acceleration = {acc.y*0.061/1000*9.81, -acc.x*0.061/1000*9.81, acc.z*0.061/1000*9.81};

    //Convert gyroscope digits to millidegrees per second, then to degrees per second, and finally to radians per second
    L3G::vector<float> angular_velocity = {gyro.y*8.75/1000*(PI/180), -gyro.x*8.75/1000*(PI/180), gyro.z*8.75/1000*(PI/180)};

    //Combine normalized magnetometer and accelerometer digits to produce Euler angles, i.e. pitch, roll, and yaw
    LSM303::vector<float> orientation = {(float)mag.x, (float)mag.y, (float)mag.z};
    orientation.x -= (magnetometer_accelerometer.m_min.x + magnetometer_accelerometer.m_max.x) / 2;
    orientation.y -= (magnetometer_accelerometer.m_min.y + magnetometer_accelerometer.m_max.y) / 2;
    orientation.z -= (magnetometer_accelerometer.m_min.z + magnetometer_accelerometer.m_max.z) / 2;
    LSM303::vector_normalize(&orientation);
    float roll = atan2(linear_acceleration.y, sqrt(pow(linear_acceleration.x,2) + pow(linear_acceleration.z,2)));
    float pitch = -atan2(linear_acceleration.x, sqrt(pow(linear_acceleration.y,2) + pow(linear_acceleration.z,2)));
    float yaw = atan2(-orientation.y*cos(roll) + orientation.z*sin(roll), orientation.x*cos(pitch) + orientation.y*sin(pitch)*sin(roll) + orientation.z*sin(pitch)*cos(roll)) + PI;
    orientation = {roll, pitch, yaw};

    //Append data to buffer
    String txBuffer = String(linear_acceleration.x) + "," +
               String(linear_acceleration.y) + "," +
               String(linear_acceleration.z) + "," +
               String(angular_velocity.x) + "," +
               String(angular_velocity.y) + "," +
               String(angular_velocity.z) + "," +
               String(orientation.x) + "," +
               String(orientation.y) + "," +
               String(orientation.z);

    return txBuffer;
  }

  return "";
}

String updateOdom() {
  String txBuffer;
  odom.update();

  txBuffer = String(odom.x) + "," +
             String(odom.y) + "," +
             String(odom.theta) + "," +
             String(odom.vx) + "," +
             String(odom.vy) + "," +
             String(odom.vtheta);

  return txBuffer;
}


////////////////////////////
////Initializer Functions///
////////////////////////////

//Initialize gyroscope, accelerometer, magnetometer, and pressure gauge
void imuInit() {
  gyroscope.init();
  gyroscope.enableDefault();
  gyroscope.setTimeout(1);

  magnetometer_accelerometer.init();
  magnetometer_accelerometer.enableDefault();
  magnetometer_accelerometer.m_min = (LSM303::vector<int16_t>){ -2494,  -3131,  -2520};
  magnetometer_accelerometer.m_max = (LSM303::vector<int16_t>){+4063,  +2462,  +2829};
  magnetometer_accelerometer.setTimeout(1);

  pressure.init();
  pressure.enableDefault();
}


////////////////////////////
////Diagnostic Functions////
////////////////////////////

//Check for valid I2C connection to verify IMU
bool imuStatus() {
  byte numberOfDevices = 0;

  for(byte address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (!error) {
      numberOfDevices++;
    }
  }

  if (numberOfDevices > 0) {
    return true;
  }
  else {
    return false;
  }
}
