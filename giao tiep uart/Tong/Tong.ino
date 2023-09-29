#include <Servo.h>

Servo myservo_in;
Servo myservo_out;
int data;
int LED=13;
int LED_in=3;
int tc = 5;
int tc_in = 4;
int count = 0;
int cambien = 6;
int cambien_out = 7;
unsigned long realtime;
unsigned long realtime_in;
unsigned long realtime_cbout;
int timewait = 100;
int timewait_in = 1;
int timewait_cbout = 100;
unsigned long timenow = 0;
unsigned long timenow_in = 0;
unsigned long timenow_cbout = 0;
unsigned long realtime_ledout;
unsigned long realtime_ledin;
int timewait_ledout = 7000;
unsigned long timenow_ledout = 0;
int timewait_ledin = 2;
unsigned long timenow_ledin = 0;

void setup() { 
  Serial.begin(115200);                              
  pinMode(LED, OUTPUT);                    
  digitalWrite (LED, LOW);                     
  pinMode(LED_in, OUTPUT);
  digitalWrite (LED_in, LOW);
  pinMode(cambien, INPUT);
  pinMode(cambien_out, INPUT);
  pinMode(tc, INPUT);
  pinMode(tc_in, INPUT);
  myservo_in.attach(11);
  myservo_out.attach(10);
  
  myservo_in.write(0);
  myservo_out.write(180);
}
void loop(){
realtime_in = millis();
if (realtime_in - timenow_in >= timewait_in){
  cambien = digitalRead(4);
  cambien_out = digitalRead(5);
}
if (cambien == LOW){
  realtime = millis();
  if (realtime - timenow >= timewait){
    timenow = millis();
    Serial.write('1');
    Led();
  }
   
}
if (cambien == HIGH){
  realtime = millis();
  if (realtime - timenow >= timewait){
    timenow = millis();
    Serial.write('0');
  }
}
if (cambien_out == LOW){
  realtime_cbout = millis();
  if (realtime_cbout - timenow_cbout >= timewait_cbout){
    timenow_cbout = millis();
    Serial.write('2');
  }
   
}
if (cambien_out == HIGH){
  realtime_cbout = millis();
  if (realtime_cbout - timenow_cbout >= timewait_cbout){
    timenow_cbout = millis();
    Serial.write('3');
  }
}
Led();
}
void Led() {
  realtime_ledin = millis();
if (realtime_ledin - timenow_ledin >= timewait_ledin){
  timenow_ledin=millis();
  data = Serial.read();
}
realtime_ledout = millis();
if (realtime_ledout - timenow_ledout >= timewait_ledout){
  timenow_ledout=millis();
  tc = digitalRead(7);
  tc_in = digitalRead(6);
  if (digitalRead(LED) == HIGH){
    Serial.print(7);
    if (tc == LOW){
    digitalWrite (LED, HIGH);
    myservo_out.write(90);
    }
    else{
    digitalWrite (LED, LOW);
    myservo_out.write(180);}
  }
  if (digitalRead(LED) == LOW){
    digitalWrite(LED, LOW);
    myservo_out.write(180);
  }
  if (digitalRead(LED_in) == HIGH){
    Serial.print(6);
    if (tc_in == LOW){
    digitalWrite (LED_in, HIGH);
    myservo_in.write(90);
    }
    else{
    digitalWrite (LED_in, LOW);
    myservo_in.write(0);
    }
  }
  if (digitalRead(LED_in) == LOW){
    digitalWrite(LED_in, LOW);
    myservo_in.write(0);
  }
}

if (data == 'L'){
  count = 1;
  if (count == 1)
  digitalWrite (LED, HIGH);
  myservo_out.write(90);
  }

if (data == 'R'){
  count = 2;
  if (count == 2)
  digitalWrite (LED_in, HIGH);
  myservo_in.write(90);
  }
  
if (data == 'N'){
  count = 0;
  if (count == 0)
  digitalWrite (LED_in, LOW);
  digitalWrite (LED, LOW);}
}
