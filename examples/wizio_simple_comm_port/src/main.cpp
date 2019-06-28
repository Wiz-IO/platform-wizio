#include <Arduino.h>
HardwareSerial Serial1("\\\\.\\COM5"); // Quectel GSM at COM5

void at_receive()
{
  Serial.print("<R> ");
  while (Serial1.available() > 0)
  {
    int b = Serial1.read(); // read
    if (b > -1)
      Serial.print((char)b); // print
  }
}

void at_send(char *command)
{
  Serial.print("<W> ");
  Serial.println(command);  // print
  Serial1.println(command); // send AT command
}

void setup()
{
  Serial.begin(); // as console
  Serial.println("[APP] Simple GSM AT commands");
  Serial1.begin(115200);
  at_send("AT");
  delay(100);
  at_receive();
  at_send("ATI");
  delay(100);
  at_receive();
  at_send("AT+GSN");
  delay(100);
  at_receive();
  at_send("AT+CCLK?");
  delay(100);
  at_receive();
}

void loop()
{
  Serial.println();
  at_send("AT");
  delay(100);
  at_receive();
  delay(5 * 1000);
}

/* RESULT:
Arduino Windows Simulator 2019 WizIO
Fri Jun 28 11:26:04 2019

[APP] Simple GSM AT commands
<W> AT
<R> AT
OK
<W> ATI
<R> ATI
Quectel
BG96
Revision: BG96MAR02A09M1G

OK
<W> AT+GSN
<R> AT+GSN
866425030081451

OK
<W> AT+CCLK?
<R> AT+CCLK?
+CCLK: "19/06/28,08:26:04+12"

OK
<W> AT
<R> AT
OK

*/