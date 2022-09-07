const int VOL_PIN = A0;
const int n = 8;
float factor[n] = { -1367.7683236907033, 4004.283865365811, -4208.839544576302, 2362.56930138958, -775.694927869914, 149.17645538165743, -15.586238303975392, 0.6836451762256601};


void setup() {
  Serial.begin( 9600 );
}

void loop() {
  long value = 0;
  float volt = 0;

  for (int i = 0; i < 100; i++) {
    value += analogRead( VOL_PIN );
  }

  volt = value / 100 * 5.0 / 1023.0;
  
  float res_angle = factor[n - 1];
  for (int i = n - 1; i > 0; i--) {
    res_angle = res_angle * volt + factor[i - 1];
  }
  
  Serial.println(String(res_angle));
  delay(100);
}
