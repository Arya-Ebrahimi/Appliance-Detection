// EmonLibrary examples openenergymonitor.org, Licence GNU GPL V3
#include "EmonLib.h"                   // Include Emon Library
EnergyMonitor emon1;                   // Create an instance

void setup()
{
  Serial.begin(9600);
  emon1.current(1, 30);
}

void print_measure(String prefix, float value, String postfix) {
  Serial.print(prefix);
  Serial.print(value, 3);
  Serial.println(postfix);
  
}

void loop()
{
  unsigned long previousMillis = millis();
  int count = 0;
  double Irms = 0;
//  while ((millis() - previousMillis) < 200)
//  {
//    Irms += emon1.calcIrms(56);  // Calculate Irms only
// 5588 samples per second
//    count++;
//  }
//  
//  Irms = Irms/count;
  Irms = emon1.calcIrms(112);
  print_measure("Irms: ", Irms, "A, ");

  

}
