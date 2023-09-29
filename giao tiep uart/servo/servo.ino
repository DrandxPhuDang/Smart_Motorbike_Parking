#include <Servo.h>

Servo myservo_in;
Servo myservo_out;

void setup() {
  myservo_in.attach(11);
  myservo_out.attach(10);
}

void loop() {
  myservo_in.write(0);
  myservo_out.write(180);
  delay(2000);
  
  myservo_in.write(90);
  myservo_out.write(90);              
  delay(2000);                   
}
