//The digital input pin that the dialer is connected to
int inputPin = 4;

//The pins the switch is connected to
int switchInput = 3;

//Constants to control the bounce and delay of the dialer - play with these to fine tune for the individular dialer
int debounceDelay = 10;
int rotationDelay = 100;

//States to keep track of actual states of the device
int prevState = LOW;
int trueState = LOW;

int prevSwitchState = LOW;
int trueSwitchState = LOW;
bool needToSendSwitch = true;
long prevStateSwitchChangeTime = 0;

//Keep track of things
int count = 0;
bool needToPrint = false;
long prevStateChangeTime = 0;

void setup() 
{
  //Startup Code:
  Serial.begin(9600);
  pinMode(inputPin, INPUT);
  pinMode(switchInput, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  trueSwitchState = digitalRead(switchInput);
}

void loop()
{
  //Main Loop Code:
  int dialReading = digitalRead(inputPin);
  int switchReading = digitalRead(switchInput);
  
  //Check to see if dial has finished rotating
  if ((millis() - prevStateChangeTime) > rotationDelay && needToPrint)
  {
    //The dial has finished spinning and needs to output its number
    Serial.println(count % 10, DEC);
    needToPrint = false;
    count = 0;
  }

  //Check to see if switch has switched
  if ((millis() - prevStateSwitchChangeTime) > rotationDelay && needToSendSwitch)
  {
    //The switch has been thrown
    if (trueSwitchState)
    {
      Serial.println("o");
    }
    else
    {
      Serial.println("-");
    }
    digitalWrite(LED_BUILTIN, !trueSwitchState);
    needToSendSwitch = false;
  }
  
  //Check to see if the input has changed at all
  if (dialReading != prevState)
  {
    //The input has changed state, get the time and then wait for the debounce delay
    prevStateChangeTime = millis();
  }

  if (switchReading != prevSwitchState)
  {
    prevStateSwitchChangeTime = millis();
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

  if ((millis() - prevStateSwitchChangeTime) > debounceDelay*10 && switchReading != trueSwitchState)
  {
    trueSwitchState = switchReading;

    needToSendSwitch = true;
  }
  
  prevState = dialReading;
  prevSwitchState = switchReading;
}
