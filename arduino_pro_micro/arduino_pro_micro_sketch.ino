#include <Keyboard.h>

const int buttonPinRed = 8;
const int buttonPinGreen = 10;
const int buttonPinBlue = 20;
const int buttonPinYellow = 15;
const int buttonPinWhite = 2;
const int buttonPinBlack = 6;


bool lastStateWhite = LOW;
bool lastStateBlack = LOW;
bool lastStateRed = LOW;
bool lastStateGreen = LOW;
bool lastStateBlue = LOW;
bool lastStateYellow = LOW;

void setup() {
  pinMode(buttonPinWhite, INPUT);
  pinMode(buttonPinBlack, INPUT);
  pinMode(buttonPinRed, INPUT);
  pinMode(buttonPinGreen, INPUT);
  pinMode(buttonPinBlue, INPUT);
  pinMode(buttonPinYellow, INPUT);

  Keyboard.begin();
}

void loop() {
  bool currentStateWhite = digitalRead(buttonPinWhite);
  bool currentStateBlack = digitalRead(buttonPinBlack);
  bool currentStateRed = digitalRead(buttonPinRed);
  bool currentStateGreen = digitalRead(buttonPinGreen);
  bool currentStateBlue = digitalRead(buttonPinBlue);
  bool currentStateYellow = digitalRead(buttonPinYellow);


  if (currentStateRed == HIGH && lastStateRed == LOW) {
    Keyboard.press('1');
    Keyboard.release('1');
  }
  lastStateRed = currentStateRed;

  if (currentStateGreen == HIGH && lastStateGreen == LOW) {
    Keyboard.press('2');
    Keyboard.release('2');
  }
  lastStateGreen = currentStateGreen;

  if (currentStateYellow == HIGH && lastStateYellow == LOW) {
    Keyboard.press('3');
    Keyboard.release('3');
  }
  lastStateYellow = currentStateYellow;

  if (currentStateBlue == HIGH && lastStateBlue == LOW) {
    Keyboard.press('4');
    Keyboard.release('4');
  }
  lastStateBlue = currentStateBlue;

  if (currentStateWhite == HIGH && lastStateWhite == LOW) {
    Keyboard.press('5');
    Keyboard.release('5');
  }
  lastStateWhite = currentStateWhite;

  if (currentStateBlack == HIGH && lastStateBlack == LOW) {
    Keyboard.press('6');
    Keyboard.release('6');
  }
  lastStateBlack = currentStateBlack;
}