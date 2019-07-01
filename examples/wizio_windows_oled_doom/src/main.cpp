#include <Arduino.h>
#include "Adafruit_GFX.h"
#include "winSSD1306.h"

/*
 KEYBOARD: Arrows and F1 ( fire )
*/

void doom_setup(void);
void doom_loop(void);
void StarWars();

void setup()
{
  Serial.begin(0);
  Serial.println("[APP] DOOM");
  pinMode(LED, OUTPUT);
#if 1
  winSSD1306 oled(0);
  oled.display();
  delay(2000);
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(WHITE);
  oled.setCursor(0, 0);
  oled.println("\n  Arduino Simulator\n");
  oled.setTextColor(WHITE, BLACK);
  oled.println("     PLATFORMIO\n");
  oled.setTextColor(BLACK, WHITE);
  oled.setCursor(10, 50);
  oled.println("   WizIO 2019     ");
  oled.display();
  oled.display();
  delay(4000);
#endif

  //StarWars();
  //doom_setup();
  oled.clearDisplay();
}

void loop()
{
  static int count = 0;
  doom_loop();
  //digitalWrite(LED, ++count % 2);
}
