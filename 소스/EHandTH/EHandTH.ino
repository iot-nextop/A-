#include <DHT.h>
#define DHTPIN 2 //온습도센서를 2번핀으로 설정
#define DHTTYPE DHT22 //온습도센서 종류설정
DHT dht (DHTPIN,DHTTYPE);



void setup() {
  Serial.begin(9600);

}

void loop() {
  delay(2000);  //2초 딜레이 설정
  int soil = analogRead(A0); //아날로그 0번핀에서 토양습도센서값을 불러온다
  int h = dht.readHumidity(); //온습도센서의 습도값을 불러온다
  int t = dht.readTemperature(); //온습도센서의 온도값을 불러온다
  Serial.print("토양습도:");
  Serial.println(soil);
  Serial.print("습도:");
  Serial.println(h);
  Serial.print("온도:");
  Serial.println(t);
  Serial.print("---------");

}
