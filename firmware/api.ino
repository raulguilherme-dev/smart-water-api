#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#define SERVER "sensor-flask.herokuapp.com"

int fluxo;

const char* ssid = "ATEL_FIBRA_27";
const char* password = "#71934263*";

void setup(void) {
  Serial.begin(9600);
  delay(10);
  Serial.println('\n');

  pinMode(4, OUTPUT);
  pinMode(14, INPUT);
  attachInterrupt(digitalPinToInterrupt(14), incInpulso, RISING);

  Serial.printf("Connecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  digitalWrite(4, HIGH);
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
  
}

void loop() {

  if (WiFi.status() == WL_CONNECTED) {
    delay(60000);
    WiFiClient client;
    HTTPClient http;    //Declare object of class HTTPClient

    StaticJsonDocument<200> doc;
    doc["sensor"] = fluxo;
  
    String requestBody;
    serializeJson(doc, requestBody);
    Serial.println(requestBody);
 
    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://sensor-flask.herokuapp.com/post"); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    int httpCode = http.POST(requestBody);

    // httpCode will be negative on error
  
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    
    http.end();  //Close connection
  } else {
    Serial.println("Desconectado");
  }
  fluxo = 0;
}

ICACHE_RAM_ATTR void incInpulso() {
  fluxo++;
}