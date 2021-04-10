#include <Keyboard.h>


void setup() {
  Keyboard.begin();
  Serial.begin(9600);
  pinMode(4, INPUT_PULLUP);
}

void loop() {

  int sensorVal = digitalRead(4);

  if (sensorVal == HIGH) {
    Keyboard.release('S');
  } else {
    Keyboard.press('S');
  }
  // put your main code here, to run repeatedly:
if (Serial.available() > 0) {
    // read incoming serial data:
    char inChar = Serial.read();
    
    if (isUpperCase(inChar)) {  // tests if myChar is an upper case letter
      Keyboard.press(inChar);
    }
    else {
      Keyboard.release(inChar);
    }
    // Type the next ASCII value from what you received:
    
  }
}
