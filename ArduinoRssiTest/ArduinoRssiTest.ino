/*
 *  Connect to a known WAP and report its RSSI constantly.
 *  If we get disconnected, try to reconnect constantly.
 */

#if defined(ARDUINO_ESP8266_ESP01) || defined(ARDUINO_ESP8266_THING)
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif

const char* ssid     = "Set me";
const char* password = "Set me";

void reportRssi(void) {
    Serial.printf("  RSSI=%d\n", WiFi.RSSI());
}

void reconnect(void) {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  reportRssi();
}

void setup() {
  Serial.begin(115200);
  delay(10);
  Serial.println();
  Serial.println();

  reconnect();
}

void loop() {
  delay(2000);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi is disconnected.  Reconnecting.");
    reconnect();
  } else {
    reportRssi();    
  }
}


