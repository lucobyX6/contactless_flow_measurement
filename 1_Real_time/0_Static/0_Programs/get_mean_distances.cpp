#include <Wire.h>
#include <SparkFun_VL53L5CX_Library.h>

// Pin definitions
#define SDA_PIN PB9
#define SCl_PIN PB8
#define LPN_PIN PB0
#define PWR_EN_PIN PC0

// VL53L5CX ToF sensor instance
SparkFun_VL53L5CX sensor;
VL53L5CX_ResultsData measurementData;

// Results
int mean_results[8][8];
volatile int round_mean =0;

// I2C speed - use 1MHz for fast data transfer
#define I2C_SPEED 1000000

void show_results();

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
      delay(1000);
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

  Tim_result->setOverflow(10000000, MICROSEC_FORMAT);
  Tim_result->attachInterrupt(&show_results);
  Tim_result->resume();

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

          mean_results[row][col] = measurementData.distance_mm[index] + mean_results[row][col];
        }
      }
    }
  }  

  // Small delay to prevent overwhelming the serial buffer
  delay(100);
  round_mean = round_mean +1;
}

void show_results()
{
  Serial.println(round_mean);
  for(int row=0; row < 8; row++)
  {
    for(int col=0; col < 8; col++)
    {
      mean_results[row][col] = mean_results[row][col]/round_mean;
      Serial.printf("%2d,%2d: %d\n", row, col, mean_results[row][col]);
    }
  }

  while(1);
}