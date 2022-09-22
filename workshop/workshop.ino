#include <Stepper.h>
#include <Keypad.h>

const unsigned long AUTO_CLOSE_TIMEOUT = 20000;
const char *REQUESTS[] = { "getcode", "setcode" };
/// Setup moteur

double stepsPerRevolution = 513;
Stepper myStepper(stepsPerRevolution, 10, 12, 11, 13);  // Pin inversion to make the library work

/// Setup pad numérique

const byte ROWS = 4;  //four rows
const byte COLS = 4;  //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};
byte rowPins[ROWS] = { 9, 8, 7, 6 };  //connect to the row pinouts of the keypad
byte colPins[COLS] = { 5, 4, 3, 2 };  //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad keypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

char pass[4];
bool doorOpened = false;
unsigned long timeOpened;
char passbuf[4];
int passlen = 0;

void setup() {
  for (int i = 0; i < 4; i++) {
    pass[i] = random(0x30, 0x3A);
  }
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();

  if (doorOpened && (millis() - timeOpened) >= AUTO_CLOSE_TIMEOUT) {
    closeDoor();
  }

  if (Serial.available() > 0) {
    String req = Serial.readStringUntil('\n');
    if (req == "getcode") {
      for (int i = 0; i < 4; i++) {
        Serial.print(pass[i]);
      }
      Serial.print('\n');
    } else if (req == "setcode") {
      String data = Serial.readStringUntil('\n');
      char arr[5];
      data.toCharArray(arr, 5);
      for (int i = 0; i < 4; i++) {
        pass[i] = arr[i];
      }
    }

  }

  if (key != NO_KEY) {
    if (key == 'A') {
      passlen = 0;
    } else if (key == 'B') {
      closeDoor();
    } else {
      passbuf[passlen] = key;
      passlen++;
    }
  }

  if (passlen == 4) {
    passlen = 0;
    if (isCodeGood()) {
      openDoor();
    }
  }
}

// Verifie si le code est bon
bool isCodeGood() {
  for (int i = 0; i < 4; i++) {
    if (pass[i] != passbuf[i]) {
      return false;
    }
  }
  return true;
}

// Ouvre/Ferme la porte
void openDoor() {
  if (!doorOpened) {
    myStepper.setSpeed(50);
    myStepper.step(stepsPerRevolution);
    doorOpened = true;
    timeOpened = millis();
  }
}
void closeDoor() {
  if (doorOpened) {
    myStepper.step(-stepsPerRevolution);
    doorOpened = false;
  }
}
