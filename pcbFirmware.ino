//FIRMWARE FOR BOTH SENSORS

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

//DEFINE IMU OBJECT
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28); 

#define fsrPin1 33 
#define fsrPin2 25
#define fsrPin3 26
#define fsrEnable 27 //put this in HIGH to make measurement and LOW when done measurement as optimized for power consumption
#define LED_RED 5
#define LED_BLUE 17
#define BatteryVoltageRead 2 //currently does nothing as resistor isnt connected but use this when reading voltage to change LED state in low battery warning

uint16_t SAMPLE_RATE = 10;


//DEFINE STATES FOR SWITCH CASING
#define PAIRING 0
#define SELECT_SIDE 101 //a
#define CALIBRATION 102 //b
#define MEASUREMENT 103 //c
#define FINISHED_MEASUREMENT 104 //d
#define ACK_PAIR    105 //e
#define FLASH_LEFT  106 //f
#define FLASH_RIGHT 107 //g
#define START_TEST 108 //h
#define SIDE_ASSIGNED 109 //i

//#define NUM_POINTS  3862 //this is what i actually can manage
//#define NUM_POINTS 12000 //this is the ideal value that i would want
#define NUM_POINTS 3000 //FOR NOW WE ARE STICKING W 30 SECONDS OF DATA COLLECTION
//FIGURED IT OUT - NEED TO DYNAMICALLY ALLOCATE THE ARRAY IN MEMORY AS STATIC ALLOCATION HAS LESS SPACE

int state = PAIRING;
float accelX[NUM_POINTS];
float accelY[NUM_POINTS];
float accelZ[NUM_POINTS];

int fsr1[NUM_POINTS];
int fsr2[NUM_POINTS];
int fsr3[NUM_POINTS];

//float angVelX[NUM_POINTS];
//float angVelY[NUM_POINTS};
//float angVelZ[NUM_POINTS];

bool ledState = false;

String reply1;
//String reply2;
//String reply3;
//String reply4;

//int counter = 0;


void setup() 
{
  // put your setup code here, to run once:
Serial.begin(115200);
SerialBT.begin("Decisionics Gait Sensor"); //Bluetooth device name
pinMode(LED_RED , OUTPUT);
pinMode(LED_BLUE, OUTPUT);

pinMode(fsrEnable, OUTPUT); 
digitalWrite(fsrEnable, LOW);

bno.begin(); // turns on the IMU

}


//ALSO NEED TO IMPLEMENT A METHOD FOR READING BATTERY VOLTAGE


void loop() 
{ //IN HERE IS WHERE THE SWITCH CASES MUST BE DEFINED, CAN WRITE FUNCTIONS OUTSIDE OF VOID LOOP THAT CAN BE CALLED FROM WITHIN

  switch(state) {

    case PAIRING:
      //if GUI button sends request, acknowledge and announce 
      
      SerialBT.println("A"); //this is to get past the time out error of waiting to write to COM3. will do a numbytesavailable type function
      
      reply1 = SerialBT.readString();
      if(reply1 == String(ACK_PAIR)) 
      {
        state = SELECT_SIDE;
      }
      break;
    
    case SELECT_SIDE:
       reply1 = SerialBT.readString();
      
       if(reply1 == String(FLASH_LEFT))
      {
        SerialBT.println("LEFT");
        
        digitalWrite(LED_RED, HIGH); //LEFT PCB WILL FLASH RED
        //delay(300);
        //digitalWrite(LED_RED, LOW);
      }
      else if(reply1 == String(FLASH_RIGHT))
      {
        SerialBT.println("RIGHT");
        
        digitalWrite(LED_BLUE, HIGH); //RIGHT PCB WILL FLASH BLUE
        //delay(300);
        //digitalWrite(LED_BLUE, LOW);
      }
      else if(reply1 == String(SIDE_ASSIGNED)) //this is sent from second purple button
      {
        state = CALIBRATION;
      }
      break;

    case CALIBRATION:
      //insert calibration code here
      calibrateData();
      break;

    case MEASUREMENT:
      for(int sampleCounter = 0; sampleCounter < NUM_POINTS; sampleCounter++)
      {
        digitalWrite(fsrEnable, HIGH); 
        
        imu::Vector<3> acc = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
        //imu::Vector<3> gyro = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);

        accelX[sampleCounter] = acc.x();
        accelY[sampleCounter] = acc.y();
        accelZ[sampleCounter] = acc.z();

        //angVelX[sampleCounter] = gyro.x();
        //angVelY[sampleCounter] = gyro.y();
        //angVelZ[sampleCounter] = gyro.z();

        fsr1[sampleCounter] = analogRead(fsrPin1);
        fsr2[sampleCounter] = analogRead(fsrPin2);
        fsr3[sampleCounter] = analogRead(fsrPin3);
        
        delay(SAMPLE_RATE);
        digitalWrite(fsrEnable, LOW); 
      }
      SerialBT.println("Measurement_Done");
      
      while(SerialBT.readString() != "Confirm"); //when what is read from serial port does not equal send_data, just wait w small delay statement
      {                                             //then when button is pushed to keep data, send message to serial port "Send_Data" and it will trigger the sendMeasurement function
        delay(5);
      }

      state = FINISHED_MEASUREMENT;
      
      //sendMeasurement(accelX, accelY, accelZ, fsr1, fsr2, fsr3);
      break;
      
    case FINISHED_MEASUREMENT:
      reply1 = SerialBT.readString();
      if(reply1 == String(START_TEST)) //this gets written from big ass start test button
      {
        state = MEASUREMENT;
      }
      else if(reply1 == "Send_Data") //this is sent from second purple button
      {
       sendMeasurement(accelX, accelY, accelZ, fsr1, fsr2, fsr3);
      }
      break;

}


}



//DEFINE SENDING MEASUREMENT FUNCTION
void sendMeasurement(float accelX[], float accelY[], float accelZ[], int fsr1[], int fsr2[], int fsr3[])
{
  for(int sampleCounter = 0; sampleCounter < NUM_POINTS; sampleCounter++)
  {
    SerialBT.print(sampleCounter);
    SerialBT.print(',');
    SerialBT.print(accelX[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(accelY[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(accelZ[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(fsr1[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(fsr2[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(fsr3[sampleCounter]);
    SerialBT.print(',');
    SerialBT.print(';');
    SerialBT.println();

    delay(1); //data seems to be coming in corrupted sometimes - hoping adding small delay helps
  }
  //state = FINISHED_MEASUREMENT;
}


//DEFINE CALIBRATION FUNCTION
void calibrateData()
{
  //define calibration variables
  uint8_t System, gyro, accel, mg = 0;
  //calibration ranges between 0-3 with 3 being best calibration
  //system represents how the calibration is as a whole including the accel, gyro, and mag
  
  bno.getCalibration(&System, &gyro, &accel, &mg);

  SerialBT.println(accel);

  delay(500);

  reply1 = SerialBT.readString();
  if(reply1 == String(START_TEST)) //this is sent by massive start test button on page 4
  { //start_test value will be sent from the start test button within the GUI which will be prompted to the user to not do until accel calibration hits 3
    state = MEASUREMENT;
    
  }

  
}
