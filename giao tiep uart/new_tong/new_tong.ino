#include <Servo.h>

Servo myservo_in;
Servo myservo_out;
int data;
int LED=13;
int LED_in=3;
int tc_out = 0;
int tc_in = 0;
int count = 0;
int cambien_in = 0;
int cambien_out = 0;
int value_barrier_in = 0;
int value_barrier_out = 0;
int dem_in = 0;
int dem_out = 3;
int dem_realtime_in = 0;
int dem_realtime_out = 0;
unsigned long realtime;
unsigned long realtime_in;
unsigned long realtime_cbout;
int timewait = 100;
int timewait_in = 1;
int timewait_cbout = 100;
unsigned long timenow = 0;
unsigned long timenow_in = 0;
unsigned long timenow_cbout = 0;
unsigned long realtime_barrier_in;
unsigned long realtime_barrier_out;
unsigned long realtime_barrier;
int timewait_barrier_in = 5000;
int timewait_barrier_out = 5000;
int timewait_barrier = 2;
unsigned long timenow_barrier_in = 0;
unsigned long timenow_barrier_out = 0;
unsigned long timenow_barrier = 0;

void setup() { 
  Serial.begin(115200);                              
  pinMode(LED, OUTPUT);                    
  digitalWrite (LED, LOW);                     
  pinMode(LED_in, OUTPUT);
  digitalWrite (LED_in, LOW);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  myservo_in.attach(11);
  myservo_out.attach(10);
  
  myservo_in.write(0);
  myservo_out.write(0);
}

void loop(){
  auto_detection();
  barrier();
}
void barrier(){
  realtime_barrier = millis();
  if (realtime_barrier - timenow_barrier>= timewait_barrier){
    timenow_barrier=millis();
    data = Serial.read();
    tc_in = digitalRead(6);
    tc_out = digitalRead(7);

  }
  if (dem_realtime_in == 1){
    realtime_barrier_in = millis();
  }
  if (realtime_barrier_in - timenow_barrier_in >= timewait_barrier_in){
    timenow_barrier_in=millis();
    if (dem_in == 1){
      if (tc_in == LOW){
        myservo_in.write(90);
        digitalWrite (LED_in, HIGH);
      }
      else{
        myservo_in.write(0);
        digitalWrite (LED_in, LOW);
        dem_in = 0;
        dem_realtime_in = 0;
      }
    }
   if (dem_in == 0){
    Serial.print("NO LOADINGGGGGGGGGGGGGGGGGG");
   }
  }
  if (dem_realtime_out == 2){
    realtime_barrier_out = millis();
  }
  if (realtime_barrier_out - timenow_barrier_out >= timewait_barrier_out){
    timenow_barrier_out=millis();
    if (dem_out == 2){
      if (tc_out == LOW){
      myservo_out.write(90);
      digitalWrite (LED, HIGH);
      }
      else{
        myservo_out.write(0);
        digitalWrite (LED, LOW);
        dem_out = 3;
        dem_realtime_out = 0;
      }
    }
    if (dem_out == 3){
      Serial.print("NO LOADINGGGGGGGGGGGGGGGGGG");
    }
  }
  if (data == 'R'){
    count = 1;
    if (count == 1)
    digitalWrite (LED, HIGH);
    myservo_out.write(90);
  }
  if (data == 'L'){
    count = 2;
    if (count == 2)
    digitalWrite (LED_in, HIGH);
    myservo_in.write(90);
  } 
  if (data == 'N'){
    count = 0;
    if (count == 0)
    digitalWrite (LED_in, LOW);
    digitalWrite (LED, LOW);
    myservo_in.write(0);
    myservo_out.write(0);
  }
}
void auto_detection(){
  realtime_in = millis();
  if (realtime_in - timenow_in >= timewait_in){
    cambien_in = digitalRead(4);
    cambien_out = digitalRead(5);
  }
  if (cambien_in == LOW){
    realtime = millis();
    if (realtime - timenow >= timewait){
      timenow = millis();
      Serial.write('1');
      dem_in = 1;
      dem_realtime_in = 1;
    }   
  }
  if (cambien_in == HIGH){
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
      dem_out = 2;
      dem_realtime_out = 2;
    }
     
  }
  if (cambien_out == HIGH){
    realtime_cbout = millis();
    if (realtime_cbout - timenow_cbout >= timewait_cbout){
      timenow_cbout = millis();
      Serial.write('3');
    }
  }
}
