#define pirPin P1_0 //PIR Sensor
#define door_sensor P1_7

int doorVal;
int doorValPrev;
int d=0, dcount=0, initd=0;
char dstr[50];

double loadValue;//Holds loadcell value
double loadValueprev;//Holds Previous Value
double lstr[50];
int l=0, lcount=0, initl=0;

int prevPir, temp=0;


//VARS
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 4;        
//the time when the sensor outputs a low impulse
unsigned int lowIn;         

//Indicates whether update is there or not i,e. 1 specifies update present and 0 specifies No Update
short int flagdoor = 1;
short int flagpir = 1;
short int flagload = 1;

//the amount of milliseconds the sensor has to be low 
//before we assume all motion has stopped
unsigned int pause = 2000;  

boolean lockLow = true;
boolean takeLowTime;  

void setup()
{
  Serial.begin(9600);
  pinMode(door_sensor, INPUT_PULLUP);
  digitalWrite(door_sensor,HIGH);
  digitalWrite(pirPin,LOW);

  pinMode(P1_3,INPUT);
  pinMode(P1_4,INPUT);
  pinMode(P1_5,INPUT);
  pinMode(P2_0,INPUT);
  pinMode(P2_1,INPUT);
  pinMode(P2_2,INPUT);
  pinMode(P2_3,INPUT);
  pinMode(P2_4,INPUT);

  pinMode(pirPin, INPUT);
  digitalWrite(pirPin, LOW);

  //give the sensor some time to calibrate
  // Serial.print("calibrating sensor ");
  for(int i = 0; i < calibrationTime; i++)
  {
    delay(1000);
  }
  // Serial.println(" done");
  // Serial.println("SENSOR ACTIVE");
  doorVal = digitalRead(door_sensor);
  //  Serial.print("D");
  //  Serial.print(doorVal);
  //  Serial.println("x");
  doorValPrev = doorVal;
  dstr[0] = doorValPrev;
  
  loadValueprev = loadValue;
  lstr[0]=loadValueprev;
}

void loop()
{
  sensorCheck();

  if(Serial.available()>0)
  {
    char ch = Serial.read();
    switch(ch)
    {
    case '2': 
      toSend();
      break;
    case '5': 
      timeOutSend();
      break;
      //    if(Serial.read()=='5')
      //    {
      //      toSend();
      //    }
      //    if(Serial.read()=='2')
      //    {
      //      timeOutSend();
      //    }
    }
  }
}

void sensorCheck()
{

  doorVal = digitalRead(door_sensor);

  if(doorVal!=doorValPrev)
  {
  //  if (digitalRead(door_sensor) == HIGH)
   // {
      dcount++;
      doorValPrev = doorVal; 
      dstr[d]= (doorValPrev == HIGH)?'1':'0';
      d++;
      flagdoor=1;
   // }
   /* if(digitalRead(door_sensor) == LOW)
    {
      dcount++;
      doorValPrev = doorVal;
      dstr[d]=doorValPrev;
      d++;
      flagdoor=1;
    }*/
  }


  int x1,x2,x3,x4,x5,x6,x7,x8;

  x1=digitalRead(12); //MSB - pin P2_4
  x2=digitalRead(11);
  x3=digitalRead(10);
  x4=digitalRead(9);
  x5=digitalRead(8);
  x6=digitalRead(7);
  x7=digitalRead(6);
  x8=digitalRead(5); //LSB - pin P1_3

  loadValue = ((128*x1)+(64*x2)+(32*x3)+(16*x4)+(8*x5)+(4*x6)+(2*x7)+(1*x8));
  if((abs(loadValue - loadValueprev))>=2 && (loadValue!= loadValueprev))
  {
    lcount++;
    loadValueprev = loadValue;
    lstr[l] = loadValueprev;
    l++;
    flagload = 1;
  }

  if(digitalRead(pirPin) == HIGH)
  {
   // prevPir = HIGH;
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

  if(digitalRead(pirPin) == LOW)
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
  lowIn =0;
}
void toSend()
{
  if(flagdoor == 1)
  {
    Serial.print("D");
    for(int z=initd; z<(dcount-initd); z++)
    {
      Serial.print(dstr[z]);
    }
    dcount=0;
    d=0;
    Serial.print("x");
  }
  if(flagload == 1)
  {
    Serial.print("C");
    for(int z=initl; z<(lcount-initl); z++)
    {
      Serial.print(lstr[z]);
      Serial.print(",");
    }
    lcount=0;
    l=0;
    Serial.print("x");
  }
  if(flagpir == 1)
  {
    Serial.print("Q");
    
      Serial.print(digitalRead(pirPin));

    Serial.print("x");      
  }
  Serial.println("M");
  flagpir = 0;
  flagdoor = 0;
  flagload = 0;
}

void timeOutSend()
{
  Serial.print("D");
  Serial.print(doorVal);
  Serial.print("x");

  Serial.print("C");
  Serial.print(loadValue);
  Serial.print("x");

  Serial.print("Q");
  Serial.print(digitalRead(pirPin));
  Serial.print("x");      

  Serial.println("M");
}
















