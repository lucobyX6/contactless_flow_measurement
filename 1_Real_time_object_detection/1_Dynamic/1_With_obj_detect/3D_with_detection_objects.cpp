#include <Wire.h>
#include <SparkFun_VL53L5CX_Library.h>
#include <HardwareTimer.h>

// Pin definitions
#define SDA_PIN PB9
#define SCl_PIN PB8
#define LPN_PIN PB0
#define PWR_EN_PIN PC0

// VL53L5CX ToF sensor instance
SparkFun_VL53L5CX sensor;
VL53L5CX_ResultsData measurementData;

// I2C speed - use 1MHz for fast data transfer
#define I2C_SPEED 1000000

// Objects identification

int matrice[8][8];
int matrice_objects[8][8];
int diff[3][3];
int value = 0;
int threshold = 100;
bool find = false; 
int group = 1;

// Functions
int abs(int entry);


void setup() {
  Serial.begin(115200); // COM 115200 bauds
  delay(3000); // Waiting for serial monitor

  Serial.println("[INFO] Initializing pins");

  // Enable power by setting PWR_EN HIGH 
  pinMode(PWR_EN_PIN, OUTPUT);
  digitalWrite(PWR_EN_PIN, HIGH);
  delay(10);

  // Enable I2C on sensor by setting LPn HIGH
  pinMode(LPN_PIN, OUTPUT);
  digitalWrite(LPN_PIN, HIGH);
  delay(10);

  // Initialize I2C with specified pins and speed
  Wire.begin();
  Wire.setClock(I2C_SPEED);

  Serial.println("[INFO] I2C ready");

  // Initialize sensor
  if (!sensor.begin()) {
    Serial.println("[ERROR] Sensor init failed");
    while (1) {
      delay(100);
    }
  }

  Serial.println("[INFO] Sensor online");

  // Configure sensor for 8x8 resolution
  sensor.setResolution(64);  // 64 zones = 8x8

  // Set ranging frequency to 15Hz (stable for continuous streaming)
  sensor.setRangingFrequency(15);

  // Start ranging
  sensor.startRanging();

  Serial.println("[INFO] Resolution 8x8 and 15kHz frequency");

  Serial.println("[INFO] Start acquisition");

  for (int row = 0; row < 8; row++) 
  {
    for (int col = 0; col < 8; col++) 
    {
      matrice[row][col] = 0;
      matrice_objects[row][col] = 0;
      if(row < 3 && col < 3)
      {
        diff[row][col] = 0;
      }
    }
  }
}

void loop() {

  
  // Check if new ToF data is available
  if (sensor.isDataReady()) {
    if (sensor.getRangingData(&measurementData)) {

      for (int row = 0; row < 8; row++) 
      {
        for (int col = 0; col < 8; col++) 
        {
          int index = row * 8 + col;

          matrice[row][col] = measurementData.distance_mm[index];
          //Serial.printf("-%d-", matrice[row][col]);
        }
      }
    }
  }  

  for (int row = 0; row < 8; row++) 
  {
    for (int col = 0; col < 8; col++) 
    {
      if(row-1 < 0 || col-1 < 0)
        diff[0][0] = 9999;
      else
        diff[0][0] = abs(matrice[row][col] - matrice[row-1][col-1]);

      if(row-1 < 0)
          diff[0][1] = 9999;
      else
          diff[0][1] = abs(matrice[row][col] - matrice[row-1][col]);

      if(row-1 < 0 or col+1 > 7)
          diff[0][2] = 9999;
      else
          diff[0][2] = abs(matrice[row][col] - matrice[row-1][col+1]);

      if(col-1 < 0)
          diff[1][0] = 9999;
      else
          diff[1][0] = abs(matrice[row][col] - matrice[row][col-1]);

      diff[1][1] = -1;

      if(col+1 > 7)
          diff[1][2] = 9999;
      else
          diff[1][2] = abs(matrice[row][col] - matrice[row][col+1]);

      if(row+1 > 7 or col-1 < 0)
          diff[2][0] = 9999;
      else
          diff[2][0] = abs(matrice[row][col] - matrice[row+1][col-1]);

      if(row+1 > 7)
          diff[2][1] = 9999;
      else
          diff[2][1] = abs(matrice[row][col] - matrice[row+1][col]);

      if(row+1 > 7 or col+1 > 7)
          diff[2][2] = 9999;
      else
          diff[2][2] = abs(matrice[row][col] - matrice[row+1][col+1]);
    
      for (int i = 0; i < 3; i++) 
      {
        for (int j = 0; j < 3; j++) 
        {
          value = diff[i][j];
          if((value != 9999 && value !=-1) && value < threshold) 
          {
            if(matrice_objects[row+i-1][col+j-1] !=0)
            {
              matrice_objects[row][col] = matrice_objects[row+i-1][col+j-1];
              find = true;
            }
              
          }  
          
        }
      }

      if(find == false)
      { 
        matrice_objects[row][col] = group;
        group ++;
      }
      else
      {
        find = false;
      }
    }
  }

  find = false;
  group = 1;
  Serial.printf("start\n");
  for (int row = 0; row < 8; row++) 
  {
    for (int col = 0; col < 8; col++) 
    {
      if(row != 7 || col != 7)
        Serial.printf("%d,%d,", matrice[row][col], matrice_objects[row][col]);
      else
        Serial.printf("%d,%d", matrice[row][col], matrice_objects[row][col]);
    
      matrice[row][col] = 0;
      matrice_objects[row][col] = 0;
      
      if(row < 3 && col < 3)
      {
        diff[row][col] = 0;
      }
    
    }

  } 
  Serial.printf("\nend\n");

  // Small delay to prevent overwhelming the serial buffer
  delay(50);
}


int abs(int entry)
{
  if(entry < 0)
    return -entry;
  else
    return entry;
  
  
}