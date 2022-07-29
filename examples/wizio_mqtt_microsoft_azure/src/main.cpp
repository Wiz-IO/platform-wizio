#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA;
#include <ClientSecure.h>
ClientSecure cs;
#include <AzureSAS.h>

// EDIT FROM YOUR PROJECT
#define AZURE_PORT          8883
#define AZURE_HOST          "<YOUR-HUB>.azure-devices.net"
#define AZURE_DEVICE_ID     "<YOUR-DEVICE-NAME>"
#define AZURE_CLIENT_ID     AZURE_DEVICE_ID
#define AZURE_USER_NAME     AZURE_HOST "/" AZURE_DEVICE_ID
#define AZURE_PRIVATE_KEY   "<YOUR-PRIVATE-KEY>"

// Nick O'Leary Library http://knolleary.net
#include <PubSubClient.h>
PubSubClient mqtt(AZURE_HOST, AZURE_PORT, cs);
/* 
  Add to project INI PubSubClient settings
  build_flags = -D MQTT_MAX_PACKET_SIZE=1024 -D MQTT_KEEPALIVE=60
*/

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Microsoft Azure...");
    AzureSAS sas(AZURE_PRIVATE_KEY, String(AZURE_HOST), utc() + 3600);
    if (mqtt.connect(AZURE_CLIENT_ID, AZURE_USER_NAME, sas.get().c_str()))
    {
      Serial.println("[MQTT] Connected");
      mqtt.publish("outTopic", "Hello world from WizIO");
      mqtt.subscribe("inTopic");
    }
    else
    {
      Serial.print("[ERROR] MQTT Connect: ");
      Serial.println(mqtt.state());
      delay(60 * 1000); // Wait retrying
    }
  }
}
void setup()
{
  Serial.begin();
  mqtt.setCallback(callback);
  //embed ClientSecure no ciphers
}

void loop()
{
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();
}