#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA; // WSAStartup
#include <ClientSecure.h>
ClientSecure cs;

void GET(Client& client, char *host, int port, char *url)
{
  Serial.printf("\n[GET] Connecting %s\n", host);
  client.connect(host, port);
  Serial.println("[GET] Send");
  client.print("GET ");
  client.print(url);
  client.print(" HTTP/1.1\r\nConnection: close\r\nHost:");
  client.print(host);
  client.print("\r\n\r\n");
  Serial.println("[GET] Receive");
  while (1)
  {
    int R = client.read();
    if (R > 0)
      Serial.print((char)R);
    else
      break;
  }
  client.stop();
  Serial.println("\n[GET] DONE");
}

void setup()
{
  Serial.begin(0);
  GET(cs, "tlstest.paypal.com", 443, "/");
}

void loop()
{
  delay(1000);
}

/* RESULT

Arduino Windows Simulator 2019 WizIO
Fri Jun 28 11:39:10 2019
[GET] Connecting tlstest.paypal.com
[GET] Send
[GET] Receive
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 20
Date: Fri, 28 Jun 2019 08:39:10 GMT
Connection: close
PayPal_Connection_OK
[GET] DONE

*/