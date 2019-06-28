#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA;
#include <EthernetClient.h>
EthernetClient cc;

// Nick O'Leary Library http://knolleary.net
#include <PubSubClient.h>
PubSubClient mqtt("iot.eclipse.org", 1883, cc); // https://iot.eclipse.org/getting-started/

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s\n", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Eclipse...");
    char client_id[64];
    snprintf(client_id, 64, "WIZIO_%d", utc()); // create unique id
    Serial.printf("[MQTT] ClientID: %s\n", client_id);
    if (mqtt.connect(client_id))
    {
      Serial.println("[MQTT] Connected");
      mqtt.publish("output", "Hello world");
      mqtt.subscribe("input");
    }
    else
    {
      Serial.printf("[ERROR] MQTT Connect: %d", (int)mqtt.state());
      delay(20000); // Wait reconnect
    }
  }
}

void setup()
{
  Serial.begin(); // as console
  mqtt.setCallback(callback);
}

void loop()
{
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();
}

/* 
  Chrome - MQTTLens
    https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm?hl=en
*/ 

