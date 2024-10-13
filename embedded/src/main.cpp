#include <Arduino.h>
// "STEP" pin for AZIMUTH
#define STEP_AZIMUTH 2
// "DIRECTION" pin for AZIMUTH
#define DIR_AZIMUTH 3
#define LIMIT_AZIMUTH 80

// "STEP" pin for AZIMUTH
#define STEP_ELEVATION 5
// "DIRECTION" pin for AZIMUTH
#define DIR_ELEVATION 6
#define LIMIT_ELEVATION 80

// PUMP relay, active high, pump on "normally open (NO) PIN"
#define PUMP_DRILL 8 

int az_steps = 40;
int el_steps = 40;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(STEP_AZIMUTH, OUTPUT);
  pinMode(DIR_AZIMUTH, OUTPUT);
  pinMode(STEP_ELEVATION, OUTPUT);
  pinMode(DIR_ELEVATION, OUTPUT);
  pinMode(PUMP_DRILL, OUTPUT);

  Serial.begin(9600);
  Serial.println("OK");
}

void step(char dir, unsigned int steps) {
  bool saturated = false;
  int step_pin = 0;
  switch(dir) {
    case 'L':
      step_pin = STEP_AZIMUTH;
      digitalWrite(DIR_AZIMUTH, HIGH);
      if(steps + az_steps >= LIMIT_AZIMUTH) {
        steps = LIMIT_AZIMUTH - az_steps;
        az_steps = LIMIT_AZIMUTH;
        saturated = true;
      } else {
        az_steps += steps;
      }
      break;
    case 'R':
      step_pin = STEP_AZIMUTH;
      digitalWrite(DIR_AZIMUTH, LOW);
      if((long) az_steps - (long) steps <= 0) {
        steps = az_steps;
        az_steps = 0;
        saturated = true;
      } else {
        az_steps -= steps;
      }
      break;
    case 'D':
      step_pin = STEP_ELEVATION;
      digitalWrite(DIR_ELEVATION, HIGH);
      if(steps + el_steps >= LIMIT_AZIMUTH) {
        steps = LIMIT_AZIMUTH - el_steps;
        el_steps = LIMIT_AZIMUTH;
        saturated = true;
      } else {
        el_steps += steps;
      }
      break;
    case 'U':
      step_pin = STEP_ELEVATION;
      digitalWrite(DIR_ELEVATION, LOW);
      if((long) el_steps - (long) steps <= 0) {
        steps = el_steps;
        el_steps = 0;
        saturated = true;
      } else {
        el_steps -= steps;
      }
      break;

  }
  while(steps > 0) {
    digitalWrite(step_pin, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(20);                      // wait for a second
    digitalWrite(step_pin, LOW);   // turn the LED off by making the voltage LOW
    delay(20); 
    steps--;
  }
  if(saturated) {
    Serial.println("Y");
  } else {
    Serial.println("L");
  }
}

unsigned int read_int() {
  return ((unsigned int) Serial.read()) << 24 | ((unsigned int) Serial.read()) << 16 | ((unsigned int) Serial.read()) << 8 | ((unsigned int) Serial.read());
}

// the loop function runs over and over again forever
void loop() {
  int avail = Serial.available();
  if(avail >= 6) {
    char cmd = '\0';
    cmd = Serial.read();

    if(cmd == 'P') {
      unsigned int pump_ms = read_int();
      if(pump_ms > 10000) {
        pump_ms = 10000;
      }
      digitalWrite(PUMP_DRILL, HIGH);
      delay(pump_ms);
      digitalWrite(PUMP_DRILL, LOW);
      Serial.println("Y");
      Serial.read();
      return;
    }
    switch(cmd) {
      case 'R':
      case 'L':
      case 'U':
      case 'D':
      unsigned int steps = read_int();
      step(cmd, steps);
      break;
      default:
      Serial.println("UNKNOWN COMMAND");
      break;
    }

    // slurps newlines
    Serial.read();
  }
  delay(500);
}

