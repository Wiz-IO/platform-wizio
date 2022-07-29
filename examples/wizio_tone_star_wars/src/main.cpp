#include <Arduino.h>

void StarWars();

void setup()
{
  Serial.println("[APP] setup");
  StarWars();
}

void loop()
{
  Serial.println("[APP] loop");
  delay(1000);
}