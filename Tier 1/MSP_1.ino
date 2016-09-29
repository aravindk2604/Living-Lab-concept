#define TempPin A4 //Temperatue Sensor
#define HumidPin A3 //Humidity Sensor
#define LumPin A6 //Luminous Sensor
#define PIRPin P1_5 //PIR Sensor
#define SmartSwitch1 P2_5 //Smart Switch1
#define SmartSwitch2 P2_4 //Smart Switch

int smartswitch1;
int smartswitchPrev1;
int scount=0,scount2=0;
int initi=0, initi2=0;
int s=0,s2=0;
char str1[50],str2[50];

int prevPir,temp=0;

int smartswitch2;
int smartswitchPrev2;

float tempthershold = 1;
float tempc = 0,tempf=0; // temperature variables
float samples[15]; // variables to make a better precision
int maxi = -100,mini = 100; // to start max/min temperature
float tempcprev = 0;

int i;//used for looping

//Indicates whether update is there or not i,e. 1 specifies update present and 0 specifies No Update
short int flagss1 = 1; 
short int flagss2 = 1;
short int flagpir = 1;
short int flaglum = 1;
short int flaghum = 1;
short int flagtemp = 1;

int luminous = 0;//holds Lumminous Sensor Raw value
int luminousprev=3;
int ch; //luminous choice for thresholding

float humi = 0;//humidity sensor raw value
float prehum = 0;
float humconst = 0;
float truehum = 0;
float truehumprev = 0;
float pretruehum = 0; 
long pretruehumconst = 0; 
long valb = 0;


//VARS
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 3;        

//the time when the sensor outputs a low impulse
unsigned int lowIn;         

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped
unsigned int pause = 2000;  

boolean lockLow = true;
boolean takeLowTime;  

//int PIRPin = 7;    //the digital pin connected to the PIR sensor's output
//int LEDPin = PF_1;


/////////////////////////////
//SETUP
void setup()
{
  Serial.begin(9600);
  //  digitalWrite(SmartSwitch1, LOW);
  //  digitalWrite(SmartSwitch2, LOW);
  digitalWrite(PIRPin, LOW);
  digitalWrite(LumPin,LOW);
  pinMode(SmartSwitch1, INPUT_PULLDOWN);
  pinMode(SmartSwitch2, INPUT_PULLDOWN);
  pinMode(PIRPin, INPUT);
  digitalWrite(PIRPin, LOW);

  //give the sensor some time to calibrate
  for(int i = 0; i < calibrationTime; i++)
  {
    delay(1000);
  }
  // Serial.println(" done");
  // Serial.println("SENSOR ACTIVE");
  smartswitch1 = digitalRead(SmartSwitch1);
  //  Serial.print("S");
  //  Serial.print(smartswitch1);
  //  Serial.println("x");
  smartswitchPrev1 = smartswitch1;
  str1[0] = smartswitchPrev1;
  smartswitch2 = digitalRead(SmartSwitch2);
  //  Serial.print("Z");
  //  Serial.print(smartswitch2);
  //  Serial.println("x");
  smartswitchPrev2 = smartswitch2;
  str2[0] = smartswitchPrev2;
}

////////////////////////////
//LOOP
void loop()
{
  sensorCheck();

  if(Serial.available()>0)
  {
    char ch = Serial.read();
    switch(ch)
    {
    case '1': 
      toSend();
      break;
    case '4': 
      timeOutSend();
      break;
    }
  }
  tempc = 0;
}

void sensorCheck()
{
  //Smartswitch checking
  smartswitch1 = digitalRead(SmartSwitch1);
  //initi = s;
  if(smartswitch1!=smartswitchPrev1)
  {
    scount++;
    smartswitchPrev1 = smartswitch1;
    str1[s] = (smartswitchPrev1==HIGH)?'1':'0' ; 
    //   Serial.println(s1[s]);
    s++;
    flagss1 = 1;

  }
  smartswitch2 = digitalRead(SmartSwitch2);
  if(smartswitch2!=smartswitchPrev2)
  {
    scount2++;
    smartswitchPrev2 = smartswitch2;
    str2[s2] = (smartswitchPrev2==HIGH)?'1':'0' ;  
    //   Serial.println(s1[s]);
    s2++;
    flagss2 = 1;

  }

  if(digitalRead(PIRPin) == HIGH)
  {

    //digitalWrite(LEDPin, HIGH);   //the led visualizes the sensors output pin state
    if(lockLow)
    {  
      //makes sure we wait for a transition to LOW before any further output is made:
      lockLow = false;
      prevPir = HIGH;
    }         
    takeLowTime = true;
    flagpir = 1;
  }

  if(digitalRead(PIRPin) == LOW)
  {       

    // digitalWrite(LEDPin, LOW);  //the led visualizes the sensors output pin state
    if(takeLowTime)
    {
      lowIn = millis();          //save the time of the transition from high to LOW
      takeLowTime = false;       //make sure this is only done at the start of a LOW phase
    }
    //if the sensor is low for more than the given pause, 
    //we assume that no more motion is going to happen
    if(!lockLow && millis() - lowIn > pause)
    {  
      //makes sure this block of code is only executed again after 
      //a new motion sequence has been detected
      lockLow = true; 
      prevPir = LOW;  
      flagpir = 1;
    }
  }
  lowIn = 0;

  //Luminous Sensor
  int lumsamples[10];
  for(int k = 0;k<10;k++)
  { 
    lumsamples[k] = analogRead(LumPin);
    luminous = luminous + lumsamples[k];
  }
  luminous = luminous/10;
 // luminous = analogRead(LumPin);
  if(luminous<=100)
  {
    ch = 0;
  }
  if(luminous>=101 && luminous<=200)
  {
    ch = 1;
  }
  if(luminous>=201 && luminous<=300)
  {
    ch = 2;
  }
  if(luminous>=301 && luminous<=400)
  {
    ch = 3;
  }
  if(luminous>=401 && luminous<=500)
  {
    ch = 4;
  }
  //  else if(luminous>560 && luminous<=660)
  //  {
  //    ch = 5;
  //  }
  //  if(luminous>660 && luminous<=850)
  //  {
  //    ch = 6;
  //  }
  //  if(luminous>850 && luminous<=1000)
  //  {
  //    ch = 7;
  //  }
  if(luminous>=500)
  {
    ch = 5;
  }
  if(ch != luminousprev)
  {
    luminousprev = ch;
      flaglum = 1;
  }
  // calculation of temperature using the analogRead
  for(i = 0;i<=14;i++)
  { 
    samples[i] = ( 3.3   * analogRead(TempPin) * 100.0) / 1024.0;
    tempc = tempc + samples[i];
  }

  tempc = tempc/15.0; 
  tempf = (tempc * 9)/ 5 + 32;

  if((abs(tempc - tempcprev))>tempthershold)
  {
    tempcprev = tempc;
    flagtemp = 1;
  }
  // Humidity sensor
  valb = analogRead(HumidPin); // humidity calculation
  prehum = (valb/5);
  humconst = (0.16/0.0062);
  humi = prehum - humconst;
  pretruehumconst = 0.00216*tempc;
  pretruehum = 1.0546-pretruehumconst;
  truehum = humi/pretruehum ;

  if((abs(truehum - truehumprev))>1)
  {
    truehumprev = truehum;
    flaghum = 1;
  }

}


//Performing the serial Write for Tier II only changed sensor values will be sent
void toSend()
{
  if(flagss1 == 1)
  {
    Serial.print("S");
    for(int z=initi; z<(scount-initi); z++)
    {
      Serial.print(str1[z]);
    }
    scount = 0;
    s=0;
    Serial.print("x");

  }
  if(flagss2 == 1)
  {
    Serial.print("Z");  
    for(int z=initi2; z<(scount2-initi2); z++)
    {
      Serial.print(str2[z]);
    }
    scount2 = 0;
    s2 = 0;
    Serial.print("x");

  }
  if(flagpir == 1 && temp!=prevPir)
  {
    Serial.print("P");

    if(temp!=prevPir)
    {
      Serial.print(digitalRead(PIRPin));
      temp = prevPir;
    }

    Serial.print("x");
  }
  if(flagtemp == 1)
  {
    Serial.print("T");
    Serial.print(tempc);
    Serial.print(",");
    Serial.print(tempf);
    Serial.print("x");
  }
  if(flaglum == 1)
  {
    Serial.print("L");
    Serial.print(ch);
    Serial.print("x");
  }
  if(flaghum == 1)
  {
    Serial.print("H");
    Serial.print (abs((long)truehum));
    Serial.print("x");      
  }
  Serial.println("M");
  flagss1 = 0;
  flagss2 = 0;
  flagpir = 0;
  flagtemp = 0;
  flaglum = 0;
  flaghum = 0;
}

// Sends all data 
void timeOutSend()
{
  Serial.print("S");
  Serial.print(smartswitch1);
  Serial.print("x");

  Serial.print("Z");
  Serial.print(smartswitch2);
  Serial.print("x");

  Serial.print("P");
  Serial.print(digitalRead(PIRPin));
  Serial.print("x");

  Serial.print("T");
  Serial.print(tempc);
  Serial.print(",");
  Serial.print(tempf);
  Serial.print("x");

  Serial.print("L");
  Serial.print(ch);
  Serial.print("x");

  Serial.print("H");
  Serial.print (abs((long)truehum));
  Serial.print("x");      

  Serial.println("M");
}












