String data="ButtonPressed";

int now;
int before;
int pressed;
const byte interruptPin = 2;
volatile bool state = false;

void setup() {
  Serial.begin(9600);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), button, LOW);
}

void loop() {
  now = millis();
  if ((state == true) && (now - before > 100)) {
    Serial.println(data);
    before = millis();
    state = false;
  }
}

void button() {
  state = true;
}
