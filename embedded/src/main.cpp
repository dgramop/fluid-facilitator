//#include "core_esp8266_features.h"
#include <Arduino.h>
#include <Stepper.h>

//#include <AFMotor.h>

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
/*void forwardstep() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep() {  
  motor1.onestep(BACKWARD, SINGLE);
}*/

//Stepper steps(200, D0, D1, D2, D3);
Stepper steps(200, 3, 4, 5, 6);

void setup()
{  
   Serial.begin(9600);           // set up Serial library at 9600 bps
   Serial.println("Stepper test!");

   // pump relay
   pinMode(7, OUTPUT);

   pinMode(3, OUTPUT);
   pinMode(4, OUTPUT);
   pinMode(5, OUTPUT);
   pinMode(6, OUTPUT);

   steps.setSpeed(60);

}


void loop()
{    
    steps.step(20);
    Serial.println("did shit");
    delay(500);
}
