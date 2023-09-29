int data;
int LED=13;
int LED_in=3;
int tc = 5;
int tc_in = 4;
int count = 0;
unsigned long realtime;
unsigned long realtime_in;
int timewait = 7000;
unsigned long timenow = 0;
int timewait_in = 1;
unsigned long timenow_in = 0;
void setup() { 
  Serial.begin(115200);                               //initialize serial COM at 9600 baudrate
  pinMode(LED, OUTPUT);                    //declare the LED pin (13) as output
  digitalWrite (LED, LOW);                     //Turn OFF the Led in the beginning
  pinMode(LED_in, OUTPUT);
  digitalWrite (LED_in, LOW);
  pinMode(tc, INPUT);
  pinMode(tc_in, INPUT);
}
void loop() {
  realtime_in = millis();
if (realtime_in - timenow_in >= timewait_in){
  timenow_in=millis();
  data = Serial.read();
}
realtime = millis();
if (realtime - timenow >= timewait){
  timenow=millis();
  tc = digitalRead(5);
  tc_in = digitalRead(4);
  if (digitalRead(LED) == HIGH){
    if (tc == LOW){
    digitalWrite (LED, HIGH);
    }
    else{
    digitalWrite (LED, LOW);}
  }
  if (digitalRead(LED) == LOW){
    digitalWrite(LED, LOW);
  }
  if (digitalRead(LED_in) == HIGH){
    if (tc_in == LOW){
    digitalWrite (LED_in, HIGH);
    }
    else{
    digitalWrite (LED_in, LOW);}
  }
  if (digitalRead(LED_in) == LOW){
    digitalWrite(LED_in, LOW);
  }
}

if (data == '1'){
  count = 1;
  if (count == 1)
  digitalWrite (LED, HIGH);}

if (data == '2'){
  count = 2;
  if (count == 2)
  digitalWrite (LED_in, HIGH);}
  
if (data == '0'){
  count = 0;
  if (count == 0)
  digitalWrite (LED_in, LOW);
  digitalWrite (LED, LOW);}
}
