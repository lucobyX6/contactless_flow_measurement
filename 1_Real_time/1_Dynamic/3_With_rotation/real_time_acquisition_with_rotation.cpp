#include <Wire.h>
#include <SparkFun_VL53L5CX_Library.h>
#include <Servo.h>

// Pin definitions
#define SDA_PIN PB9
#define SCl_PIN PB8
#define LPN_PIN PB0
#define PWR_EN_PIN PC0
#define PWM_SERVO_PIN PB10

// VL53L5CX ToF sensor instance
SparkFun_VL53L5CX sensor;
VL53L5CX_ResultsData measurementData;

// DF9GMS servo motor instance
Servo servo_tof;

// I2C speed - use 1MHz for fast data transfer
#define I2C_SPEED 1000000

// Angle °
int angle =0;
int direction =1;

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

  // Servomotor
  servo_tof.attach(PWM_SERVO_PIN); 
  Serial.println("[INFO] Servo ready");

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

  Serial.println("[INFO] Start communication");
}

void loop() {

  Serial.printf("start\n");

  // Check if new ToF data is available
  if (sensor.isDataReady()) {
    if (sensor.getRangingData(&measurementData)) {
      Serial.printf("%d\n", angle);
      // Send all value using serial port
      for (int row = 0; row < 8; row++) 
      {
        for (int col = 0; col < 8; col++) 
        {
          int index = row * 8 + col;

          Serial.printf("%d, %d, %d\n", row, col, measurementData.distance_mm[index]);
        }
      }
    }
  }  
  Serial.printf("end\n");

  // Small delay to prevent overwhelming the serial buffer
  delay(50);

  angle = angle + direction;
  servo_tof.write(angle);  
  if(angle >= 180)
  {
    while(1);
    direction = -1;
  }
  if(angle <= 0)
  {
    direction = 1;
  }
}