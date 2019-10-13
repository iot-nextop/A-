#include <DHT.h> //온습도센서를 사용하기위해 전용라이브러리를 불러온다
#define DHTPIN 13 //온습도센서를 13번핀으로 설정
#define DHTTYPE DHT22 //온습도센서 종류설정
#define pump 12 //펌프용
DHT dht (DHTPIN,DHTTYPE);
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>

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
const char* password ="20183365";
#define FIREBASE_HOST "smartfarm-1681b.firebaseio.com"
#define FIREBASE_AUTH "Xwn0dRhbU7Sa8xMr4Z87R7z2Mc3Xz9jmyoIrcKxg"
int FB_h;
int FB_t;
int FB_soil;
int FB_pump;

WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);

  //펌프용
  pinMode(pump, OUTPUT);

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

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  FB_soil = Firebase.getInt("earthhumidity");
  FB_h = Firebase.getInt("humidity");
  FB_t = Firebase.getInt("temperature");
  FB_pump = Firebase.getInt("pump");
  
}
 
void loop() {
  //센서
  int soil = analogRead(A0); //아날로그 0번핀에서 토양습도센서값을 불러온다
  int h = dht.readHumidity(); //온습도센서의 습도값을 불러온다
  int t = dht.readTemperature(); //온습도센서의 온도값을 불러온다
  int cds = digitalRead(12);//


  
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){

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
  client.println("<body>");

  client.println("<table border=1 width=300 height=300>");
  client.println("<tr>");
  client.println("<th>soil:<b> ");
  client.println(soil);
  client.println("</b></th>");
  client.println("</tr>");


  client.println("<tr>");
  client.println("<th>temp:<b> ");
  client.println(t);
  client.println("</b></th>");
  client.println("</tr>");
  
  client.println("<tr>");
  client.println("<th>humi:<b> ");
  client.println(h);
  client.println("</b></th>");
  client.println("</tr>");

  client.println("<tr>");
  client.println("<th>pump(on:1//off:0) : <b> ");
  client.println(FB_pump);
  client.println("</b></th>");
  client.println("</tr>");
  
  client.println("</table>");

  client.println("</body>");

  client.println("<a href=\"/C\"><button>button </button></a>");
  client.println("<a href=\"/P\"><button>pumpON </button></a>");
  client.println("<a href=\"/Pf\"><button>pumpOFF </button></a>");
  //client.println("<a href=\"?cmd=RELOAD_soil\"><button>soil</button></a>");
  //client.println("<a href=\"?cmd=RELOAD_t\"><button>temp</button></a>");
  //client.println("<a href=\"?cmd=RELOAD_h\"><button>humi</button></a>");


  client.println("</html>");

  if (request.indexOf("GET /C")>=0)
  {
      FB_soil = soil;
      FB_t = t;
      FB_h = h;
      Firebase.pushInt("earthhumidity",FB_soil);
      Firebase.pushInt("temperature",FB_t);
      Firebase.pushInt("humidity",FB_h);
      Serial.println("check");
  }


  
  if (request.indexOf("GET /P")>=0)
  {
   digitalWrite(pump, HIGH);
   FB_pump = 1;
   Firebase.setInt("pump",FB_pump);
  }

  if (request.indexOf("GET /Pf")>=0)
  {
   digitalWrite(pump, LOW);
   FB_pump = 0;
   Firebase.setInt("pump",FB_pump);
  }

 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}
