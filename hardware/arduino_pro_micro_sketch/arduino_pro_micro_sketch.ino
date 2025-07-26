/*
Скетч для прошивки Arduino Pro Micro в качестве контроллера кнопок игроков.
Чип ATmega32u4 имеет аппаратную поддержку USB 2.0, поэтому при подключении по USB
контроллер будет восприниматься хостом как внешняя USB-клавиатура, а нажатие на игровую кнопку будет
интерпретироваться как нажатие на кнопку клавиатуры.
Установка дополнительных драйверов не требуется.

Внимание! В данном скетче отсутствует защита от "дребезга" контактов.
Предполагается, что эта защита реализована аппаратно в схеме контроллера.
*/

#include <Keyboard.h>

// Назначаем кнопкам пины на плате Arduino
const int buttonPinRed = 8;
const int buttonPinGreen = 10;
const int buttonPinBlue = 15;
const int buttonPinYellow = 20;
const int buttonPinWhite = 2;
const int buttonPinBlack = 6;

// Задаем начальное состояние кнопок
bool lastStateWhite = LOW;
bool lastStateBlack = LOW;
bool lastStateRed = LOW;
bool lastStateGreen = LOW;
bool lastStateBlue = LOW;
bool lastStateYellow = LOW;

void setup() {
  // Настраиваем пины кнопок как вход сигнала
  pinMode(buttonPinWhite, INPUT);
  pinMode(buttonPinBlack, INPUT);
  pinMode(buttonPinRed, INPUT);
  pinMode(buttonPinGreen, INPUT);
  pinMode(buttonPinBlue, INPUT);
  pinMode(buttonPinYellow, INPUT);

  Keyboard.begin();
}

void loop() {
  // Считываем состояние кнопок
  bool currentStateWhite = digitalRead(buttonPinWhite);
  bool currentStateBlack = digitalRead(buttonPinBlack);
  bool currentStateRed = digitalRead(buttonPinRed);
  bool currentStateGreen = digitalRead(buttonPinGreen);
  bool currentStateBlue = digitalRead(buttonPinBlue);
  bool currentStateYellow = digitalRead(buttonPinYellow);

  // Отправляем на хост сигнал нажатия кнопок
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
