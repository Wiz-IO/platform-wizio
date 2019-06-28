#include <Arduino.h>
#include <Ethernet.h>
Ethernet WSA;

#include <jwt.h>
#include <CloudIoTCore.h>

// EDIT FROM YOUR PROJECT
#define GOOGLE_DEVICE       "<your-device>"
#define GOOGLE_LOCATION     "<your-location>"
#define GOOGLE_PROJECT      "<your-project-name>"
#define GOOGLE_REGISTRY     "<your-registry>"
#define GOOGLE_CLIENT "projects/" GOOGLE_PROJECT "/locations/" GOOGLE_LOCATION "/registries/" GOOGLE_REGISTRY "/devices/" GOOGLE_DEVICE

// Create folder for certificates and download it
#define CERT_PATH "D:\\CERTS\\"
/*
  https://cloud.google.com/iot/docs/how-tos/mqtt-bridge
  Download Googles CA certificates for "mqtt.googleapis.com" to D:\CERT
  The complete Google root CA 
    https://pki.goog/roots.pem

  https://cloud.google.com/iot/docs/how-tos/mqtt-bridge#using_a_long-term_mqtt_domain
  Download long-term primary and backup for "mqtt.2030.ltsapis.goog" to D:\CERT
    https://pki.goog/gtsltsr/gtsltsr.crt
    https://pki.goog/gsr4/GSR4.crt
  Convert to PEM and split at one file "google_long_ca.pem"
*/

#define HOST_NAME "mqtt.googleapis.com" /* or "mqtt.2030.ltsapis.goog for long-term */
#if 0
#define GOOGLE_CA_LIST CERT_PATH "roots.pem"
#else
#define GOOGLE_CA_LIST CERT_PATH "google_long_ca.pem"
#endif

#define GOOGLE_CIPHERS "ECDHE-ECDSA-AES128-GCM-SHA256"

/* 
To get the private key run (where private-key.pem is the ec private key
used to create the certificate uploaded to google cloud iot):
  openssl ec -in <private-key.pem> -noout -text
and copy priv: part.
The key length should be exactly the same as the key length bellow (32 pairs
of hex digits). If it's bigger and it starts with "00:" delete the "00:". If
it's smaller add "00:" to the start. If it's too big or too small something
is probably wrong with your key.
*/
#define PRIVATE_KEY "6e:b8:17:35:c7:fc:6b:d7:a9:cb:cb:49:7f:a0:67:" \
                    "63:38:b0:90:57:57:e0:c0:9a:e8:6f:06:0c:d9:ee:" \
                    "31:41"

CloudIoTCoreDevice goo(GOOGLE_PROJECT, GOOGLE_LOCATION, GOOGLE_REGISTRY, GOOGLE_DEVICE, PRIVATE_KEY);

/* 
  Add to project INI
  build_flags = -D MQTT_MAX_PACKET_SIZE=1024 -D MQTT_KEEPALIVE=60
*/
#include <PubSubClient.h>
#include <ClientSecure.h>
ClientSecure cs;
PubSubClient mqtt(HOST_NAME, 8883, cs);

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Google IoT Core...");
    String jwt = goo.createJWT(utc());
    if (mqtt.connect(GOOGLE_CLIENT, "unused", jwt.c_str()))
    {
      Serial.println("[MQTT] Connected");
      /* See your google topics */
      mqtt.publish("outTopic", "Hello world");
      mqtt.subscribe("inTopic");
    }
    else
    {
      Serial.printf("[ERROR] MQTT Connect: %s\n", mqtt.state());
      delay(10 * 000); // Wait retrying
    }
  }
}

void setup()
{
  Serial.begin(0);
  Serial.println("[APP] Google IoT Core - PubSubClient");
  mqtt.setCallback(callback);
  cs.setSNI(HOST_NAME);
  cs.setCiphers(GOOGLE_CIPHERS);
  cs.setCACert(GOOGLE_CA_LIST);
}

void loop()
{
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();
}
