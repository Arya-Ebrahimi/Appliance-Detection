const float FACTOR = 30;
const float VMIN = 1.08;
const float VMAX = 3.92;

const float ADCV = 5.0;

void setup() {

  Serial.begin(9600);
  
}

void print_measure(String prefix, float value, String postfix) {
  Serial.print(prefix);
  Serial.print(value, 3);
  Serial.println(postfix);
  
}

void loop() {

  float current_rms = get_corriente();
  float power = 230.0 * current_rms;

  print_measure("Irms: ", current_rms, "A, ");
  delay(1000);
  
  
}


float get_corriente() {
  float volt;
  float c;
  float sum = 0;
  long t = millis();

  int counter = 0;

  while(millis() - t < 500){
    volt = analogRead(A1) * ADCV / 1023.0;
    c = f(volt, VMIN, VMAX, -FACTOR, FACTOR);

    sum += sq(c);
    counter++;
    delay(1);

    
  }

  c = sqrt(sum / counter);
  return(c);

  
}


float f (float x, float in_min, float in_max, float out_min, float out_max) {
  return (x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
