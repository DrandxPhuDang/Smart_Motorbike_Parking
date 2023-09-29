int tc_in = 5;
int tc_out = 6; 
int tc_servo_in = 4; 
int tc_servo_out = 7;

void setup() {
  Serial.begin(115200);
  pinMode(tc_in, INPUT);
  pinMode(tc_out, INPUT);
  pinMode(tc_servo_in, INPUT);
  pinMode(tc_servo_out, INPUT);

}

void loop() {
  tc_in = digitalRead(5);
  tc_out = digitalRead(6);
  tc_servo_in = digitalRead(4);
  tc_servo_out = digitalRead(7);
  if (tc_in == LOW){
    Serial.println("check in");
  }
  if (tc_out == LOW){
    Serial.println("check out");
  }
  if (tc_servo_in == LOW){
    Serial.println("Open para in");
  }
  if (tc_servo_out == LOW){
    Serial.println("Open para out");
  }
}
