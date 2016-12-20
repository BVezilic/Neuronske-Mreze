const int backPin = 7;
const int frontPin = 8;
const int leftPin = 12;
const int rightPin = 13;

int incomingByte;

void setup() {
  Serial.begin(9600);
  pinMode(frontPin, OUTPUT);
  pinMode(backPin, OUTPUT);
  pinMode(leftPin, OUTPUT);
  pinMode(rightPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == '0') {
      digitalWrite(frontPin, HIGH);
    } 
    if (incomingByte == '1') {
      digitalWrite(frontPin, LOW);
    }
    if (incomingByte == '2'){
      digitalWrite(backPin, HIGH);  
    }
    if (incomingByte == '3'){
      digitalWrite(backPin, LOW);  
    }
    if (incomingByte == '4'){
      digitalWrite(leftPin, HIGH);  
    }
    if (incomingByte == '5'){
      digitalWrite(leftPin, LOW);  
    }
    if (incomingByte == '6'){
      digitalWrite(rightPin, HIGH);  
    }
    if (incomingByte == '7'){
      digitalWrite(rightPin, LOW);  
    }
  }
}
