#include <Servo.h>
#define SERVO 9

Servo servo;
void setup() {
  servo.attach(SERVO);
  servo.write(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  servo.write(0);
  delay(200);
}
