/*
  Serial Call and Response
  Language: Wiring/Arduino

  This program sends an ASCII A (byte of value 65) on startup and repeats that
  until it gets some data in. Then it waits for a byte in the serial port, and
  sends three sensor values whenever it gets a byte in.

  The circuit:
  - potentiometers attached to analog inputs 0 and 1
  - pushbutton attached to digital I/O 2

  created 26 Sep 2005
  by Tom Igoe
  modified 24 Apr 2012
  by Tom Igoe and Scott Fitzgerald
  Thanks to Greg Shakar and Scott Fitzgerald for the improvements

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/SerialCallResponse
*/


#define P1 7
#define P2 8

int inByte = 0;         // incoming serial byte

unsigned long lastReceivedTime;

void setup() {
  // start serial port at 9600 bps:
  Serial.begin(9600);

  pinMode(P1, OUTPUT);   // digital sensor is on digital pin 2
  pinMode(P2, OUTPUT);

  delay(10);

  digitalWrite(P1, HIGH);
  digitalWrite(P2, HIGH);

  lastReceivedTime = millis();

}

void loop() {
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {

    lastReceivedTime = millis();

    // get incoming byte:
    inByte = Serial.read();
    if (inByte == 0x2B) {
      digitalWrite(P1, LOW);
      digitalWrite(P2, HIGH);
    }
    else if (inByte == 0x2D) {
      digitalWrite(P1, HIGH);
      digitalWrite(P2, LOW);
    }
    else {
      digitalWrite(P1, HIGH);
      digitalWrite(P2, HIGH);
    }
  }
  else if (millis() > lastReceivedTime + 30000) {
    digitalWrite(P1, HIGH);
    digitalWrite(P2, HIGH);
  }
}
