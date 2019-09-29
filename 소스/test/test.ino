#include <DHT.h> //온습도센서를 사용하기위해 전용라이브러리를 불러온다
#define DHTPIN 13 //온습도센서를 13번핀으로 설정
#define DHTTYPE DHT22 //온습도센서 종류설정
DHT dht (DHTPIN,DHTTYPE);
#include <ESP8266WiFi.h>

/*
 * Original Code from:
 * http://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/
 * By:  Magesh Jayakumar 
 * 
 * Modified By: C.J. Windisch
 * Modified On: * 08/24/2017
 * Modification: Added code to read from analog photo sensor to demonstrate reading input over WIFI.
 */
 
const char* ssid = "Nextop1";
const char* password = "20183365";
 


WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}
 
void loop() {
  //센서
  int soil = analogRead(A0); //아날로그 0번핀에서 토양습도센서값을 불러온다
  int h = dht.readHumidity(); //온습도센서의 습도값을 불러온다
  int t = dht.readTemperature(); //온습도센서의 온도값을 불러온다

  
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){

    Serial.println(",");
    //delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Always update the photocell value anytime there's a request
  // NOTE: We have the cmd=RELOAD_PHOTOCELL command because we need a way
  // to update the photocell without changing the led state for the user

  
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  //client.println( "Refresh: 20");        // refresh the page automatically every 20 sec
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");


  
  client.println("<p>토양습도:<b> ");
  client.println(soil);
  client.println("</b></p>");

  client.println("<p>온도:<b> ");
  client.println(t);
  client.println("</b></p>");
  
  client.println("<p>습도:<b> ");
  client.println(h);
  client.println("</b></p>");
  
  client.println("<a href=\"?cmd=RELOAD_soil\"><button>EH</button></a>");
  client.println("<a href=\"?cmd=RELOAD_t\"><button>t</button></a>");
  client.println("<a href=\"?cmd=RELOAD_h\"><button>h</button></a>");

  client.println("</html>");
 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}
