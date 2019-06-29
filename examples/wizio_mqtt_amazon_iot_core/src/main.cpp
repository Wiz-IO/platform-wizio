#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA;
#include <ClientSecure.h>
ClientSecure cs;

// Create folder for certificates
#define CERT_PATH "D:\\CERTS\\"

/*
  Amazon IoT Core - Manage
  Create Thing and Certificates, download it and Activate
  Policies Allow
  Interact - get HTTPS URL for host name
*/

// EDIT FROM YOUR THING
#define AWS_PORT 8883
#define AWS_HOST "<YOUR>-ats.iot.us-east-2.amazonaws.com"
#define AWS_CERTIFICATE CERT_PATH "<YOUR>-certificate.pem.crt"
#define AWS_PRIVATE_KEY CERT_PATH "<YOUR>-private.pem.key"
//#define AWS_CA_FILE CERT_PATH "AmazonRootCA1.pem"

// Nick O'Leary Library http://knolleary.net
#include <PubSubClient.h>
/* 
  Add to project INI PubSubClient settings
  build_flags = -D MQTT_MAX_PACKET_SIZE=1024 -D MQTT_KEEPALIVE=60
*/
PubSubClient mqtt(AWS_HOST, AWS_PORT, cs);


void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Amazon...");
    if (mqtt.connect("client_arduino"))
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
  cs.setCertificate(AWS_CERTIFICATE);
  cs.setPrivateKey(AWS_PRIVATE_KEY);
}

void loop()
{
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();
}