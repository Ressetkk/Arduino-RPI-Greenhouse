#include <DHT.h>
#include <DHT_U.h>
#include <RTClib.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// define pins for easier recognition
#define dht_pin 3
#define temp_pin 4
#define in1_pin 6
#define in2_pin 7
#define in3_pin 8
#define in4_pin 9
#define soil_pin A0

#define PACKET_SIZE 19

// Libraries initialization

RTC_DS1307 rtc;
DHT dht(dht_pin, DHT11);
OneWire oneWire(temp_pin);
DallasTemperature ds_sensor(&oneWire);

// those values we will modify
byte temp_value = 26;
byte soil_value = 70;
byte temp_range = 1;
bool in1_state = 1; // LED power state

// those will stay unharmed
float ds_temp;  // in Celsius
float dht_hum;  // percentage
float dht_temp; // in Celsius
byte soil;      // percentage
bool in2_state = 0;
bool in3_state = 0;

byte I2CPacket[PACKET_SIZE];

int prev_hour = -9999;
int hours = 0;
int hour_diff;

union float2bytes_t 
{ 
  float f; 
  byte b[sizeof(float)]; 
};

void setup() {
  Wire.begin(3);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  if (! rtc.begin()) {
    while(1);
  }
  if (!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  pinMode(in1_pin, OUTPUT);
  pinMode(in2_pin, OUTPUT);
  pinMode(in3_pin, OUTPUT);
  digitalWrite(in1_pin, HIGH);
  digitalWrite(in2_pin, HIGH);
  digitalWrite(in3_pin, HIGH);
}

void loop() {
  DateTime now = rtc.now();
  delay(1000);
  ds_sensor.requestTemperatures();
  dht_hum = dht.readHumidity();
  dht_temp = dht.readTemperature();
  int soil_read = analogRead(soil_pin);
  soil = 100 - (float(soil_read) / 1023 * 100);
  ds_temp = ds_sensor.getTempCByIndex(0);

  if ((!in1_state) && (digitalRead(in1_pin) == 1)) {
    digitalWrite(in1_pin, LOW);
  }
  else if((in1_state) && (digitalRead(in1_pin) == 0)) {
    digitalWrite(in1_pin, HIGH);
  }
  
  if (dht_temp > (temp_value + temp_range)) {
    digitalWrite(in3_pin, HIGH);
    in3_state = false;
  }
  else if (dht_temp < (temp_value - temp_range)) {
    digitalWrite(in3_pin, LOW);
    in3_state = true;
  }

  
  if (soil < (soil_value - 3)) {
    hours = now.hour();
    hour_diff = hours - prev_hour;
    if (hour_diff < 0) {
      prev_hour += 24;
    }
    if (hour_diff >= 1) {
      digitalWrite(in2_pin, LOW);
      in2_state = true;
      delay(1000);
      digitalWrite(in2_pin, HIGH);
      in2_state = false;
      prev_hour = hours;
    }
  }
}

void requestEvent() {
  setI2Cpacket();
  Wire.write(I2CPacket, PACKET_SIZE);
}

void receiveEvent(int howMany) {
  Wire.read();
  if (Wire.available()) getI2CPacket();
}

void setI2Cpacket() {

  // Externel Temperature
  float2bytes_t ds_t;
  ds_t.f = ds_temp;
  I2CPacket[0] = ds_t.b[0];
  I2CPacket[1] = ds_t.b[1];
  I2CPacket[2] = ds_t.b[2];
  I2CPacket[3] = ds_t.b[3];

  // DHT temperature
  float2bytes_t dht_t;
  dht_t.f = dht_temp;
  I2CPacket[4] = dht_t.b[0];
  I2CPacket[5] = dht_t.b[1];
  I2CPacket[6] = dht_t.b[2];
  I2CPacket[7] = dht_t.b[3];

  //DHT humidity
  float2bytes_t dht_h;
  dht_h.f = dht_hum;
  I2CPacket[8] = dht_h.b[0];
  I2CPacket[9] = dht_h.b[1];
  I2CPacket[10] = dht_h.b[2];
  I2CPacket[11] = dht_h.b[3];

  // soil humidity
  I2CPacket[12] = soil;

  // in1_pin state
  I2CPacket[13] = in1_state;
  
  // in2_pin state
  I2CPacket[14] = in2_state;
  
  // in3_pin state
  I2CPacket[15] = in3_state;

  // wanted temperature
  I2CPacket[16] = temp_value;

  // wanted humidity
  I2CPacket[17] = soil_value;

  // temperature range from -x to x
  I2CPacket[18] = temp_range;

}

void getI2CPacket() {
  if (Wire.available()) {
    temp_value = Wire.read();
    soil_value = Wire.read();
    temp_range = Wire.read();
    in1_state = Wire.read();
  }
}

