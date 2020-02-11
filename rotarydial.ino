//The digital input pin that the dialer is connected to
int inputPin = 2;

//Constants to control the bounce and delay of the dialer - play with these to fine tune for the individular dialer
int debounceDelay = 10;
int rotationDelay = 100;

//States to keep track of actual states of the device
int prevState = LOW;
int trueState = LOW;

//Keep track of things
int count = 0;
bool needToPrint = false;
long prevStateChangeTime = 0;

void setup() 
{
  //Startup Code:
  Serial.begin(9600);
  pinMode(inputPin, INPUT);
  
}

void loop()
{
  //Main Loop Code:
  int dialReading = digitalRead(inputPin);
  
  //Check to see if dial has finished rotating
  if ((millis() - prevStateChangeTime) > rotationDelay && needToPrint)
  {
    //The dial has finished spinning and needs to output its number
    Serial.println(count % 10, DEC);
    needToPrint = false;
    count = 0;
  }
  
  //Check to see if the input has changed at all
  if (dialReading != prevState)
  {
    //The input has changed state, get the time and then wait for the debounce delay
    prevStateChangeTime = millis();
  }
  
  //If the state has changed, wait for the debounce time to finish, then check if it is a real state change
  if ((millis() - prevStateChangeTime) > debounceDelay && dialReading != trueState)
  {
    //Debounce time is up, and the state has acutally changed
    trueState = dialReading;
    
    if (trueState == HIGH)
    {
      //If the state went from LOW -> HIGH, increase the count of the number
      count++;
      needToPrint = true;
    }
  }
  
  prevState = dialReading;
}

