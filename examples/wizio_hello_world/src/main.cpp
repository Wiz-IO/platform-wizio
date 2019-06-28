#include <Arduino.h>

void setup()
{
  Serial.begin(); // as console
  Serial.print("[APP] ");
  Serial.println("Hello World");
}

void loop()
{
  Serial.printf("[APP] Loop: %d\n", seconds());
  delay(5 * 1000);
}