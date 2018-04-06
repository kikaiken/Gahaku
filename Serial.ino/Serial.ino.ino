#include <ArduinoJson.h>
#include <VarSpeedServo.h>


VarSpeedServo s1;
VarSpeedServo s2;
VarSpeedServo s3;
VarSpeedServo s4;

void parse_json(){
  char buff[200] = {0};
  while(Serial.available() == 0){
    delay(1);
  }
  String str;
  if(Serial.available()>0){
    str = Serial.readStringUntil(';');
  }
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& recv = jsonBuffer.parseObject(str);
  if(!recv.success()){
    //String json_sen ="{\"status\":\"Failed\"}\n";
    Serial.print("MS");
  }else{
    int servo1 = recv["Servo1"];
    int servo2 = recv["Servo2"];
    int servo3 = recv["Servo3"];    
    int servo4 = recv["Servo4"];
    s1.write(servo1,5,false);
    s2.write(servo2,60,false);
    s3.write(servo3,40,false);
    s4.write(servo4,20,false);
    int value = analogRead(A0);
    String val = String(0);
    //String json_sen = String("{\"status\":\"OK\",\"battery\":"+val+"}\n");
    Serial.print("OK");
  }
  
}

void setup()  {
  Serial.begin(76800);
  s1.attach(3);
  s2.attach(5);
  s3.attach(6);
  s4.attach(9);
}

void loop() {
  parse_json();
}
