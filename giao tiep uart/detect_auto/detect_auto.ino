int data;
int LED=13;
int LED_in=3;
int tc = 5;
int tc_in = 4;
int count = 0;
int cambien = 6;
unsigned long realtime;
unsigned long realtime_in;
int timewait = 100;
unsigned long timenow = 0;
int timewait_in = 1;
unsigned long timenow_in = 0;
void setup() { 
  Serial.begin(115200);                              
  pinMode(LED, OUTPUT);                    
  digitalWrite (LED, LOW);                     
  pinMode(LED_in, OUTPUT);
  digitalWrite (LED_in, LOW);
  pinMode(cambien, INPUT);
  pinMode(tc, INPUT);
  pinMode(tc_in, INPUT);
}
void loop(){
realtime_in = millis();
if (realtime_in - timenow_in >= timewait_in){
  cambien = digitalRead(6);
}
if (cambien == LOW){
  realtime = millis();
  if (realtime - timenow >= timewait){
    timenow = millis();
    Serial.write('1');
  } 
}
if (cambien == HIGH){
  realtime = millis();
  if (realtime - timenow >= timewait){
    timenow = millis();
    Serial.write('0');
  }
}
}
