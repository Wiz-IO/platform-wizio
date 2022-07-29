#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA; // WSAStartup
#include <EthernetClient.h>
EthernetClient cc;

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
  GET(cc, "wizio.eu", 80, "/iot.php");
}

void loop()
{
  delay(1000);
}

/* RESULT

Arduino Windows Simulator 2019 WizIO
Fri Jun 28 11:35:57 2019
[GET] Connecting wizio.eu
[GET] Send
[GET] Receive
HTTP/1.1 200 OK
Date: Fri, 28 Jun 2019 08:35:59 GMT
Server: Apache
Upgrade: h2,h2c
Connection: Upgrade, close
Cache-Control: max-age=0
Expires: Fri, 28 Jun 2019 08:35:59 GMT
Content-Length: 47
Content-Type: text/html
[WIZIO.EU] Hello World ( 2019-06-28 11:35:59 )
[GET] DONE

*/