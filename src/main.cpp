#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#include "readysite.h"

constexpr char sta_ssid[] = "ssid";
constexpr char sta_password[] = "password";

constexpr char ap_ssid[] = "RemoteFixerESP";
constexpr char ap_password[] = "password";


constexpr uint32_t bufUARTsize = 1024*10;
uint8_t bufUART[bufUARTsize]{0};
uint32_t bufUARTindex = 0;
uint32_t bufUARTindexSend = 0;

inline void initWiFi()
{
  WiFi.begin(sta_ssid, sta_password);

  // WiFi.mode(WIFI_STA);
  // WiFi.disconnect();
  // delay(100);
  
  // WiFi.softAPConfig(IPAddress(192,168,4,1), IPAddress(192,168,4,1), IPAddress(255,255,255,0));
  // WiFi.softAP(ap_ssid, ap_password);
}

ESP8266WebServer server(80);

inline void serverConfig()
{
  server.on("/", HTTP_GET, [](){
    server.sendHeader("Content-Encoding", "gzip");
    server.send(200,"text/html", websiteContent, websiteSize);
  });

  server.on("/getUARTdata", HTTP_POST, [](){
    server.send(200, "text", bufUART, bufUARTindex - bufUARTindexSend);
  });

  server.begin();
}

void setup() 
{
  initWiFi();

  Serial.begin(9600);
  serverConfig();
}

void loop() 
{
  if(int32_t availableBytes = Serial.available() > 0)
  {
    uint32_t tmp = static_cast<uint32_t>(availableBytes);
    if(bufUARTindex + tmp > bufUARTsize)
      bufUARTindex = 0;

    uint32_t bytesCount = Serial.readBytes(&(bufUART[bufUARTindex]), tmp);
    if(tmp == bytesCount)
      ;//good

    bufUARTindex += bytesCount;
  }

  server.handleClient();
}
