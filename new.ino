const int nPin_soil = A0;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:

}

void loop() {

  int soil = analogRead(nPin_soil);

  Serial.print("sensor : ");
  Serial.println(soil);
  delay(1000);
  // put your main code here, to run repeatedly:

}
