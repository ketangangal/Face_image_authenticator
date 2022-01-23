#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

const char* ssid = "wifiname";
const char* password = "Password";

int relayInput = 2;

void setup() {
  Serial.begin(115200); 
  pinMode(relayInput, OUTPUT);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
  if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;
      http.begin(client,  "http://c67b-14-97-167-154.ngrok.io/deviceon");
      
      int httpResponseCode = http.GET();
        
      if (httpResponseCode>0) {
         Serial.print("HTTP Response code: ");
         Serial.println(httpResponseCode);
         String payload = http.getString();
         Serial.println(payload);
         digitalWrite(relayInput, HIGH);
         delay(5000);
         http.begin(client,  "http://c67b-14-97-167-154.ngrok.io/deviceoff");
         int httpResponseCode = http.GET();
         if (httpResponseCode>0) {
         Serial.print("HTTP Response code: ");
         Serial.println(httpResponseCode);
         String payload = http.getString();
         Serial.println(payload);
         digitalWrite(relayInput, LOW);
         delay(5000);}
         else {
          Serial.print("Error code: ");
          Serial.println(httpResponseCode);
        }
         
         }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
        }
        // Free resources
        http.end();
      }
    else {
      Serial.println("WiFi Disconnected");
    }
  delay(5000);
 }
