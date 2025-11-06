/*
========================
  Project to get coord by soccers and publish in MQTT 
========================
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <TinyGPS++.h>

/* ====== DEVICE MAPPING ====== */
#define RXD2 16                                        /*<-- RX pin for GPS module */
#define TXD2 17                                        /*<-- TX pin for GPS module */

#define GPS_BAUD 9600                                  /*<-- Baud rate for GPS communication */


/* ====== CONNECTION SETTING ====== */

const char* default_SSID = "";                         /*<-- Your WiFi network name */
const char* default_PASSWORD = "";                     /*<-- Password for WiFi network */
const char* default_BROKER_MQTT = "";                  /*<-- MQTT broker address */
const int default_BROKER_PORT = 1883;                  /*<-- MQTT broker port */

WiFiClient espClient;                                  /*<-- WiFi client for network connection */
PubSubClient MQTT(espClient);                          /*<-- MQTT client instance */
HardwareSerial gpsSerial(2);                           /*<-- Serial port for GPS communication */
TinyGPSPlus gps;                                       /*<-- GPS parser object */

/* ====== BROKER CONFIGURATIONS ====== */
const char* default_TOPIC_COORDINATES = "/TEF/device/sc"; /*<-- MQTT topic for publishing coordinates */

/* ====== MUTABLE VARIABLES ======*/

char* SSID = const_cast<char*>(default_SSID);           /*<-- WiFi network name (mutable) */
char* PASSWORD = const_cast<char*>(default_PASSWORD);   /*<-- WiFi password (mutable) */
char* BROKER_MQTT = const_cast<char*>(default_BROKER_MQTT); /*<-- MQTT broker address (mutable) */
int BROKER_PORT = default_BROKER_PORT;                  /*<-- MQTT broker port */
char* TOPIC_COORDINATES = const_cast<char*>(default_TOPIC_COORDINATES); /*<-- Coordinates publication topic */
String team = "";
String player = "";

void initSerial(){
  /*Initialize Serial communication for debugging*/
  Serial.begin(115200);
}

void initWiFi(){
  /*Initialize WiFi connection*/
  delay(10);
  Serial.println("------ WiFi Connection ------");
  Serial.print("Connecting to network: ");
  Serial.println(SSID);
  Serial.print("Please wait");
  reconectWiFi();
}

void reconectWiFi(){
  /*Reconnect to WiFi network if disconnected*/
  if (WiFi.status() == WL_CONNECTED){
    return;
  }
  WiFi.begin(SSID, PASSWORD);
  while(WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Successfully connected!");
  Serial.print("Network: ");
  Serial.println(SSID);
  Serial.print("Obtained IP: ");
  Serial.println(WiFi.localIP());
}

void initMQTT(){
  /*Configure MQTT client settings and server connection*/
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
}

void reconnectMQTT(){
  /*Reconnect to MQTT broker if connection is lost*/
  while (!MQTT.connected()){
    Serial.print("Connecting to MQTT broker...");
    if (MQTT.connect("GOAL_Client")){
      Serial.println("Connected to MQTT broker!");
    } else {
      Serial.print("Failed to connect, rc= ");
      Serial.println(MQTT.state());
      Serial.println(" retrying in 5 seconds...")
      delay(5000);
    }
  }
}

void checkWiFiAndMQTTConnections(){
  /* Verify and reconnect WiFi and MQTT connections */
    if (!MQTT.connected())
      reconnectMQTT();
    reconectWiFi();
}


void setup() {
  /* Main initialization function - runs once at startup */
  initSerial();                                      /* <-- Initialize serial communication */
  initWiFi();                                        /* <-- Connect to WiFi network */
  initMQTT();                                        /* <-- Configure MQTT client */
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2); /* <-- Initialize GPS serial communication */
  delay(5000);                                       /* <-- Wait 5 seconds for system stabilization */
}

void loop() {
  checkWiFiAndMQTTConnections();                      /* <-- Check the WiFi and MQTT connection */
  gpsCommunication();                                 /* <-- Read and process GPS coordinates */
  MQTT.loop();                                        /* <-- Maintain MQTT connection */ 
  delay(500);                                         /* <-- Avoid overloading the serial monitor */ 
}


void gpsCommunication(){
  /* Read GPS data and publish coordinates via MQTT */
  unsigned long start = millis();                    /* <-- Record start time for GPS reading */
  bool coordinatesPublished = false;                 /* <-- Control variable for publication status */
  
  while(millis() - start < 5000 && !coordinatesPublished){
    /* Continue for 5 seconds or until coordinates are published */
    while (gpsSerial.available() > 0){
      /* Process all available GPS data */
      gps.encode(gpsSerial.read());                  /* <-- Decode GPS NMEA data */
    }

    if (gps.location.isUpdated() && gps.location.isValid()){
      /* Check if valid coordinates are available */
      String lat = String(gps.location.lat(), 6);    /* <-- Format latitude with 6 decimal places */
      String lng = String(gps.location.lng(), 6);    /* <-- Format longitude with 6 decimal places */
      String coord = lat + "," + lng + "," + team + "," + player;                /* <-- Combine coordinates into single string */

      if (MQTT.publish(TOPIC_COORDINATES, coord.c_str())) {
        /* Publish coordinates to MQTT topic */
        coordinatesPublished = true;                 /* <-- Mark publication as successful */
        Serial.println("Published coordinates = ");  /* <-- Print confirmation message */
        Serial.println(coord);                       /* <-- Display published coordinates */
      }
    }
    delay(10);                                       /* <-- Small delay to prevent CPU overload */
  }
}