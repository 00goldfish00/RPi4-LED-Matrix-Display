//Test Code
//Written by Samson Segovia

//LED INFO
#include <FastLED.h>

#define DATA_PIN    3
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    600
#define ARRAY_SIZE(A) (sizeof(A) / sizeof((A)[0]))    //Used for Party
CRGB leds[NUM_LEDS];
uint8_t fadinpartyHue = random8();
uint8_t rainbowHue = random8();
uint8_t snakeHue = random8();
uint8_t oboh = random8();    //One-by_One Hue
uint8_t obos = 220;   //One-by-One Saturation
uint8_t brightVar =96;

#define BRIGHTNESS          96
#define FRAMES_PER_SECOND  120    //Smooths out LEDs

//Arrow Code
//     *
//      * *
//  * * * * *
//      * *
//      *
uint8_t arrow[8] = {0x00, 0x04 ,0x06, 0x1f, 0x06, 0x04, 0x00};


//LCD Setup
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  

//Joystick Setup
const int SW_pin = 2; // digital pin connected to switch output
const int X_pin = 0; // analog pin connected to X output
const int Y_pin = 1; // analog pin connected to Y output

//Mic Setup
const int micPin  = 4;

//Variables
int option = 1;
bool screenLock = false;
int menu = 0;
int optionColor = 0;
int bright = 9;       
int density = 10;      //(1/densityVar) amount of lights lit up
int densityVar = 1;   //mapped density from 10 to 1 -> 1 to 10
int bvd = 0;          //bright vs density variable
int sped = 5;         //fading color speed
int spedVal = 150;
int ssped = 3;   //snake speed
int micVal = 0;
int randColor = 0;
unsigned long sleepTime = 18000000;        //Time to sleep at 
unsigned long currentTime = 0;      //Current time since arduino turned on
unsigned long targetTime = 18000000;       //targetTime = currentTime + sleepTime
unsigned long currentTimeHolder = 0;        //Holds time when sleepTime is set
int sleep = 5;


void setup() {
    delay(1500); //1.5 seconds delay for recovery
    //LED Setup
    FastLED.addLeds<LED_TYPE,DATA_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);    //IDK why .setCorrection(TypicalLEDStrip; is there
    FastLED.setBrightness(BRIGHTNESS);                  //Setting Initial Brightness
    FastLED.setCorrection(UncorrectedColor);
    
    // Setup Serial Monitor
    Serial.begin (9600);
   
    //Initializes LCD Starting Menu 
    lcd.init();
    lcd.backlight();
    lcd.createChar(0, arrow); 
    lcd.setCursor(0,1); 
    lcd.write(0);
    lcd.setCursor(3,0);
    lcd.print("Choose Setting:");
    lcd.setCursor(2,1);  
    lcd.print("Solid Color");
    lcd.setCursor(2,2);  
    lcd.print("Fading Colors");
    lcd.setCursor(2,3);  
    lcd.print("Sync to Music");

    //JoyStick Button Initialize
    pinMode(SW_pin, INPUT);
    digitalWrite(SW_pin, HIGH);
    Serial.begin(9600);

    //Mic Initialize
    pinMode(micPin, INPUT);
}


//Party Arrays and Variables Used in Methods
// List of patterns to cycle through.  Each is defined as a separate function below.
typedef void (*SimplePatternList[])();
SimplePatternList gPatterns = {confetti};

uint8_t gCurrentPatternNumber = 0; // Index number of which pattern is current
uint8_t partyHue = 0; // rotating "base color" used by many of the patterns



void loop() { 
    sleepFunction();
    FastLED.delay(1000/FRAMES_PER_SECOND);          //Smoothing Out LEDs
    switch(option){            //Submenu Options
        case 1:
            if(analogRead(Y_pin) > 750){    //down
                lcd.clear();
                lcd.setCursor(0,2); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Choose Setting:");
                lcd.setCursor(2,1);  
                lcd.print("Solid Color");
                lcd.setCursor(2,2);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,3);  
                lcd.print("Sync to Music");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){     //up
                //Nothing bc at top of menu 
            }
            if((option == 1) && (analogRead(X_pin) > 750)){       //Submenu Color Setup
                lcd.clear();
                lcd.setCursor(0,1); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Select a Color:");
                lcd.setCursor(2,1);  
                lcd.print("White");
                lcd.setCursor(2,2);  
                lcd.print("Pink");
                lcd.setCursor(2,3);  
                lcd.print("Hot Pink");
                menu = 1;
                optionColor = 1;
                delay(350);
            }
            while(menu == 1){         //Submenu Color Options
                sleepFunction();
                switch(optionColor){
                    case 1:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,2); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Select a Color:");
                            lcd.setCursor(2,1);  
                            lcd.print("White");
                            lcd.setCursor(2,2);  
                            lcd.print("Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Hot Pink");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            //Nothing bc at top of menu
                        }
                        if(analogRead(X_pin) < 250){    //Takes you back to main menu     //Needed in every option
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(255,255,255);                          //White     
                            }               
                            FastLED.show();    
                        }
                    break;    
                    case 2:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Select a Color:");
                            lcd.setCursor(2,1);  
                            lcd.print("White");
                            lcd.setCursor(2,2);  
                            lcd.print("Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Hot Pink");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Select a Color:");
                            lcd.setCursor(2,1);  
                            lcd.print("White");
                            lcd.setCursor(2,2);  
                            lcd.print("Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Hot Pink");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                                leds[x].setRGB(255,20,147);                         //Pink     
                            }               
                        FastLED.show();              
                        }
                    break;
                    case 3:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("White");
                            lcd.setCursor(2,1);  
                            lcd.print("Pink");
                            lcd.setCursor(2,2);  
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Red");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,2); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Select a Color:");
                            lcd.setCursor(2,1);  
                            lcd.print("White");
                            lcd.setCursor(2,2);  
                            lcd.print("Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Hot Pink");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(224,5,97);                            //Hot Pink     
                            }               
                            FastLED.show();    
                        }                        
                    break;
                    case 4:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Pink");
                            lcd.setCursor(2,1);  
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,2);  
                            lcd.print("Red");
                            lcd.setCursor(2,3);  
                            lcd.print("Orange");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Select a Color:");
                            lcd.setCursor(2,1);  
                            lcd.print("White");
                            lcd.setCursor(2,2);  
                            lcd.print("Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Hot Pink");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){   
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x] = CRGB::Red;                            //Red    
                            }               
                            FastLED.show();                                     
                        }                        
                    break;
                    case 5:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,1);  
                            lcd.print("Red");
                            lcd.setCursor(2,2);  
                            lcd.print("Orange");
                            lcd.setCursor(2,3);  
                            lcd.print("Yellow");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("White");
                            lcd.setCursor(2,1);  
                            lcd.print("Pink");
                            lcd.setCursor(2,2);  
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,3);  
                            lcd.print("Red");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(255,20,0);                            //Orange     
                            }               
                            FastLED.show();                                                                                                                                        
                        }
                    break;             
                    case 6:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Red");
                            lcd.setCursor(2,1);  
                            lcd.print("Orange");
                            lcd.setCursor(2,2);  
                            lcd.print("Yellow");
                            lcd.setCursor(2,3);  
                            lcd.print("Lime");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Pink");
                            lcd.setCursor(2,1);  
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,2);  
                            lcd.print("Red");
                            lcd.setCursor(2,3);  
                            lcd.print("Orange");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(255,74,0);                            //Yellow     
                            }               
                            FastLED.show();                                                                     
                        }                        
                    break;               
                    case 7:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Orange");
                            lcd.setCursor(2,1);  
                            lcd.print("Yellow");
                            lcd.setCursor(2,2);  
                            lcd.print("Lime");
                            lcd.setCursor(2,3);  
                            lcd.print("Green");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Hot Pink");
                            lcd.setCursor(2,1);  
                            lcd.print("Red");
                            lcd.setCursor(2,2);  
                            lcd.print("Orange");
                            lcd.setCursor(2,3);  
                            lcd.print("Yellow");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(110,255,0);                            //Lime     
                            }               
                            FastLED.show();                             
                        }                                       
                    break;        
                    case 8:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Yellow");
                            lcd.setCursor(2,1);  
                            lcd.print("Lime");
                            lcd.setCursor(2,2);  
                            lcd.print("Green");
                            lcd.setCursor(2,3);  
                            lcd.print("Turquoise");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Red");
                            lcd.setCursor(2,1);  
                            lcd.print("Orange");
                            lcd.setCursor(2,2);  
                            lcd.print("Yellow");
                            lcd.setCursor(2,3);  
                            lcd.print("Lime");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(0,255,0);                            //Green     
                            }               
                            FastLED.show();                               
                        }                                       
                    break; 
                    case 9:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Lime");
                            lcd.setCursor(2,1);  
                            lcd.print("Green");
                            lcd.setCursor(2,2);  
                            lcd.print("Turquoise");
                            lcd.setCursor(2,3);  
                            lcd.print("Cyan");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Orange");
                            lcd.setCursor(2,1);  
                            lcd.print("Yellow");
                            lcd.setCursor(2,2);  
                            lcd.print("Lime");
                            lcd.setCursor(2,3);  
                            lcd.print("Green");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(64,224,208);                            //Turquoise     
                            }               
                            FastLED.show();                                                                                                 
                        }               
                    break;      
                    case 10:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Green");
                            lcd.setCursor(2,1);  
                            lcd.print("Turquoise");
                            lcd.setCursor(2,2);  
                            lcd.print("Cyan");
                            lcd.setCursor(2,3);  
                            lcd.print("Blue");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Yellow");
                            lcd.setCursor(2,1);  
                            lcd.print("Lime");
                            lcd.setCursor(2,2);  
                            lcd.print("Green");
                            lcd.setCursor(2,3);  
                            lcd.print("Turquoise");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(0,128,128);                            //Cyan     
                            }               
                            FastLED.show();                                                     
                        }               
                    break;   
                    case 11:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Turquoise");
                            lcd.setCursor(2,1);  
                            lcd.print("Cyan");
                            lcd.setCursor(2,2);  
                            lcd.print("Blue");
                            lcd.setCursor(2,3);  
                            lcd.print("Indigo");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Lime");
                            lcd.setCursor(2,1);  
                            lcd.print("Green");
                            lcd.setCursor(2,2);  
                            lcd.print("Turquoise");
                            lcd.setCursor(2,3);  
                            lcd.print("Cyan");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x] = CRGB::Blue;                                //Blue     
                            }               
                            FastLED.show();                             
                        }               
                    break;               
                    case 12:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Cyan");
                            lcd.setCursor(2,1);  
                            lcd.print("Blue");
                            lcd.setCursor(2,2);  
                            lcd.print("Indigo");
                            lcd.setCursor(2,3);  
                            lcd.print("Purple");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Green");
                            lcd.setCursor(2,1);  
                            lcd.print("Turquoise");
                            lcd.setCursor(2,2);  
                            lcd.print("Cyan");
                            lcd.setCursor(2,3);  
                            lcd.print("Blue");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(43,0,130);                            //Indigo     
                            }               
                            FastLED.show();                              
                        } 
                    break;      
                    case 13:
                        if(analogRead(Y_pin) > 750){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Blue");
                            lcd.setCursor(2,1);  
                            lcd.print("Indigo");
                            lcd.setCursor(2,2);  
                            lcd.print("Purple");
                            lcd.setCursor(2,3);  
                            lcd.print("Violet");
                            optionColor++;
                            delay(150);
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Turquoise");
                            lcd.setCursor(2,1);  
                            lcd.print("Cyan");
                            lcd.setCursor(2,2);  
                            lcd.print("Blue");
                            lcd.setCursor(2,3);  
                            lcd.print("Indigo");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(96,0,128);                            //Purple     
                            }               
                            FastLED.show();                                                        
                        }                         
                    break;   
                    case 14:
                        if(analogRead(Y_pin) > 750){
                            //Nothing bc at bottom of color submenu
                        }
                        else if(analogRead(Y_pin) < 250){
                            lcd.clear();
                            lcd.setCursor(0,3); 
                            lcd.write(0);
                            lcd.setCursor(2,0);
                            lcd.print("Cyan");
                            lcd.setCursor(2,1);  
                            lcd.print("Blue");
                            lcd.setCursor(2,2);  
                            lcd.print("Indigo");
                            lcd.setCursor(2,3);  
                            lcd.print("Purple");
                            optionColor--;
                            delay(150);
                        }
                        if(analogRead(X_pin) < 250){        
                            lcd.clear(); 
                            lcd.setCursor(0,1); 
                            lcd.write(0);
                            lcd.setCursor(3,0);
                            lcd.print("Choose Setting:");
                            lcd.setCursor(2,1);  
                            lcd.print("Solid Color");
                            lcd.setCursor(2,2);  
                            lcd.print("Fading Colors");
                            lcd.setCursor(2,3);  
                            lcd.print("Sync to Music");
                            menu = 0;
                            option = 1;
                            optionColor = 0;
                            delay(150);
                        }
                        if(digitalRead(SW_pin) == 0){
                            fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
                            for(int x = 0; x < NUM_LEDS; x += densityVar){
                               leds[x].setRGB(155,38,182);                            //Violet     
                            }               
                            FastLED.show();                               
                        }                         
                    break;                                                                                                                     
                }     //End Color Submenu
            }       //End of when submenu = 1
        break;
        case 2:                             //Fading Colors
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Choose Setting:");
                lcd.setCursor(2,1);  
                lcd.print("Solid Color");
                lcd.setCursor(2,2);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,3);  
                lcd.print("Sync to Music");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,1); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Choose Setting:");
                lcd.setCursor(2,1);  
                lcd.print("Solid Color");
                lcd.setCursor(2,2);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,3);  
                lcd.print("Sync to Music");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){           //Clicking "Fading Colors" Option
                lcd.clear();
                lcd.setCursor(4,1);
                lcd.print("Relax & Vibe");   
                menu = 5;  
                fill_solid(leds, NUM_LEDS, CRGB::Black);    //pre-set to Black
            }
            while(menu == 5){
                sleepFunction();
                for(int x = 0; x < NUM_LEDS; x += densityVar){      //For loop for densityVar
                    leds[x] = CHSV(fadinpartyHue,255,255);
                    EVERY_N_MILLIS_I(spedMethod,spedVal){   //Special EVERY_N case          //Equation for finding the correct ms per hue is -> ms = (period * 1000)/255    //255 = number of hues
                        fadinpartyHue++;                                                    //Since sped (speed variable) is only 1-10, ms can only be from 30-300
                    }                                                                       //If you want to change this you can find the period which you would like by using -> period = (ms * 255)/1000 
                    spedMethod.setPeriod(spedVal);  //used method made from line 900
                }
                FastLED.show();                                                         //Then if you are satisfied with the period time, you can change (330 - (sped * 30) to -> (((11 * max ms)/10) - (sped * (.1 * max ms)))
                if(analogRead(X_pin) < 250){
                    lcd.clear();
                    lcd.setCursor(0,2); 
                    lcd.write(0);
                    lcd.setCursor(3,0);
                    lcd.print("Choose Setting:");
                    lcd.setCursor(2,1);  
                    lcd.print("Solid Color");
                    lcd.setCursor(2,2);  
                    lcd.print("Fading Colors");
                    lcd.setCursor(2,3);  
                    lcd.print("Sync to Music");
                    menu = 0;
                    delay(150);
                }
            }
        break;
        case 3:                               //Sync to Music
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Solid Color");
                lcd.setCursor(2,1);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,2);  
                lcd.print("Sync to Music");
                lcd.setCursor(2,3);  
                lcd.print("Party");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,2); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Choose Setting:");
                lcd.setCursor(2,1);  
                lcd.print("Solid Color");
                lcd.setCursor(2,2);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,3);  
                lcd.print("Sync to Music");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){             //Clicking "Sync to Music" Option
                lcd.clear();
                lcd.setCursor(2,1);
                lcd.print("Listen to Music!");                
                menu = 4;
                fill_solid(leds, NUM_LEDS, CRGB::Black);    //pre-set to Black                
            }
            while(menu == 4){                        //Music/Color Fluxuation
                sleepFunction();
                micVal = digitalRead(micPin);
                for(int x = 0; x < NUM_LEDS; x += densityVar){      //For loop for densityVar
                    if(micVal == 0){
                        leds[x] = CHSV(randColor,255,255);    //Picks random color everytime it turns on
                    }
                    else{
                        leds[x] = CHSV(0,0,0);  //Black
                    }
                    EVERY_N_MILLISECONDS(150){
                        randColor = random8();
                    }
                }
                FastLED.show();
                if(analogRead(X_pin) < 250){
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(3,0);
                    lcd.print("Choose Setting:");
                    lcd.setCursor(2,1);  
                    lcd.print("Solid Color");
                    lcd.setCursor(2,2);  
                    lcd.print("Fading Colors");
                    lcd.setCursor(2,3);  
                    lcd.print("Sync to Music");
                    menu = 0;
                    delay(150);                                                         
                }
            }
        break;
        case 4:                             //Party
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Fading Colors");
                lcd.setCursor(2,1);  
                lcd.print("Sync to Music");
                lcd.setCursor(2,2);  
                lcd.print("Party");
                lcd.setCursor(2,3);  
                lcd.print("Rainbow");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(3,0);
                lcd.print("Choose Setting:");
                lcd.setCursor(2,1);  
                lcd.print("Solid Color");
                lcd.setCursor(2,2);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,3);  
                lcd.print("Sync to Music");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){           //Clicking "Party" Option
                lcd.clear();
                lcd.setCursor(6,1);
                lcd.print("Partyyy!");   
                menu = 6;  
            }
            while(menu == 6){
                sleepFunction();
                // Call the current pattern function once, updating the 'leds' array
                gPatterns[gCurrentPatternNumber]();
                // send the 'leds' array out to the actual LED strip
                FastLED.show();  
                // do some periodic updates
                EVERY_N_MILLISECONDS( 15 ) { partyHue++; } // slowly cycle the "base color" through the rainbow
                //EVERY_N_SECONDS( 10 ) { nextPattern(); } // change patterns periodically
                if(analogRead(X_pin) < 250){
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("Solid Color");
                    lcd.setCursor(2,1);  
                    lcd.print("Fading Colors");
                    lcd.setCursor(2,2);  
                    lcd.print("Sync to Music");
                    lcd.setCursor(2,3);  
                    lcd.print("Party");
                    menu = 0;
                    delay(150);
                }
            }
        break;
        case 5:                           //Rainbow
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Sync to Music");
                lcd.setCursor(2,1);  
                lcd.print("Party");
                lcd.setCursor(2,2);  
                lcd.print("Rainbow");
                lcd.setCursor(2,3);  
                lcd.print("Snake");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Solid Color");
                lcd.setCursor(2,1);  
                lcd.print("Fading Colors");
                lcd.setCursor(2,2);  
                lcd.print("Sync to Music");
                lcd.setCursor(2,3);  
                lcd.print("Party");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){           //Clicking "Rainbow" Option
                lcd.clear();
                lcd.setCursor(6,1);
                lcd.print("Rainbow");   
                menu = 7;  
                fill_solid(leds, NUM_LEDS, CRGB::Black);    //pre-set to Black
            }
            while(menu == 7){
                sleepFunction();
                for(int x = 0; x < NUM_LEDS; x += densityVar){
                    leds[x] = CHSV(rainbowHue + (x * 4),255,255);  //i * n -> this changed length of each color (higher = shorter)
                }
                EVERY_N_MILLISECONDS(17){   //The ms changes the pace at which the colors move (low = faster)
                    rainbowHue++;
                }
                FastLED.show();
                if(analogRead(X_pin) < 250){
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("Fading Colors");
                    lcd.setCursor(2,1);  
                    lcd.print("Sync to Music");
                    lcd.setCursor(2,2);  
                    lcd.print("Party");
                    lcd.setCursor(2,3);  
                    lcd.print("Rainbow");
                    menu = 0;
                    delay(150);
                }
            }
        break;
        case 6:                           //Snake
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Party");
                lcd.setCursor(2,1);  
                lcd.print("Rainbow");
                lcd.setCursor(2,2);  
                lcd.print("Snake");
                lcd.setCursor(2,3);  
                lcd.print("One-by-One");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Fading Colors");
                lcd.setCursor(2,1);  
                lcd.print("Sync to Music");
                lcd.setCursor(2,2);  
                lcd.print("Party");
                lcd.setCursor(2,3);  
                lcd.print("Rainbow");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){           //Clicking "Snake" Option
                lcd.clear();
                lcd.setCursor(7,1);
                lcd.print("Snake");   
                menu = 8;  
            }
            while(menu == 8){
                sleepFunction();
                fadeToBlackBy( leds, NUM_LEDS, 20);
                int pos = beatsin16(ssped, 0, NUM_LEDS-1 ); //ssped changes the speed (higher is faster)
                leds[pos] += CHSV( snakeHue, 255, 192);    //192 changes brightness?
                FastLED.show();
                snakeHue++;
                if(analogRead(X_pin) < 250){
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("Sync to Music");
                    lcd.setCursor(2,1);  
                    lcd.print("Party");
                    lcd.setCursor(2,2);  
                    lcd.print("Rainbow");
                    lcd.setCursor(2,3);  
                    lcd.print("Snake");
                    menu = 0;
                    delay(150);
                }
            }
        break;
        case 7:                           //One-by-One
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Snake");
                lcd.setCursor(2,1);  
                lcd.print("One-by-One");
                lcd.setCursor(2,2);  
                lcd.print("");
                lcd.setCursor(2,3);  
                lcd.print("Brightness");
                option++;
                delay(150);
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Sync to Music");
                lcd.setCursor(2,1);  
                lcd.print("Party");
                lcd.setCursor(2,2);  
                lcd.print("Rainbow");
                lcd.setCursor(2,3);  
                lcd.print("Snake");
                option--;
                delay(150);
            }
            if(digitalRead(SW_pin) == 0){           //Clicking "One-by-One" Option
                lcd.clear();
                lcd.setCursor(8,1);
                lcd.print("Spin");   
                menu = 11;  
                fill_solid(leds, NUM_LEDS, CRGB::Black);                //pre-set Black
            }
            while(menu == 11){
                sleepFunction();
                for(int x = 0; x < NUM_LEDS; x += densityVar){
                    leds[x] = CHSV(oboh, obos, 255);    //Picks random color everytime it turns on     
                    FastLED.show();
                    if(analogRead(X_pin) < 250){
                        lcd.clear();
                        lcd.setCursor(0,3); 
                        lcd.write(0);
                        lcd.setCursor(2,0);
                        lcd.print("Party");
                        lcd.setCursor(2,1);  
                        lcd.print("Rainbow");
                        lcd.setCursor(2,2);  
                        lcd.print("Snake");
                        lcd.setCursor(2,3);  
                        lcd.print("One-by-One");
                        menu = 0;
                        delay(150);
                    }
                }            
                oboh += random8(24,48);
                obos = random8(180,255);                  
            }
        break;
        case 8:                                   //Brightness 
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("One-by-One");
                lcd.setCursor(2,1);  
                lcd.print("");
                lcd.setCursor(2,2);  
                lcd.print("Brightness");
                lcd.setCursor(2,3);  
                lcd.print("Fading Speed");
                option++;
                delay(150); 
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Party");
                lcd.setCursor(2,1);  
                lcd.print("Rainbow");
                lcd.setCursor(2,2);  
                lcd.print("Snake");
                lcd.setCursor(2,3);  
                lcd.print("One-by-One");
                option--;
                delay(350);
            }
            if(analogRead(X_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,1);
                lcd.write(0);
                lcd.setCursor(1,1);
                lcd.print("Brightness: ");
                lcd.print(bright);
                lcd.setCursor(1,3);
                lcd.print("Density: 1/");
                lcd.print(densityVar);
                bvd = 1;
                menu = 2;
            }
            while(menu == 2){
                sleepFunction();
                while(bvd == 1){
                    if((analogRead(Y_pin) > 750) && (bright > 1)){
                        bright--;
                        brightVar = map(bright,1,10,10,100);      //Could've just used bright * 10, but I'm expiramenting 
                        FastLED.setBrightness(brightVar);
                        FastLED.show();
                        lcd.clear();
                        lcd.setCursor(0,1);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        delay(200);
                    }
                    else if((analogRead(Y_pin) < 250) && (bright < 10)){
                        bright++;
                        brightVar = map(bright,1,10,10,100);
                        FastLED.setBrightness(brightVar);
                        FastLED.show();
                        lcd.clear();
                        lcd.setCursor(0,1);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        delay(200);
                    }
                    if(digitalRead(SW_pin) == 0){
                        lcd.clear();
                        lcd.setCursor(0,3);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        bvd = 2;        
                        delay(150);             
                    }
                    if(analogRead(X_pin) < 250){
                        lcd.clear();
                        lcd.setCursor(0,3); 
                        lcd.write(0);
                        lcd.setCursor(2,0);
                        lcd.print("Snake");
                        lcd.setCursor(2,1);  
                        lcd.print("One-by-One");
                        lcd.setCursor(2,2);  
                        lcd.print("");
                        lcd.setCursor(2,3);  
                        lcd.print("Brightness");
                        bvd = 0;
                        menu = 0;
                        delay(150);
                    }
                }
                while(bvd == 2){
                    if((analogRead(Y_pin) > 750) && (density > 1)){
                        density--;
                        densityVar = map(density,1,10,10,1);
                        lcd.clear();
                        lcd.setCursor(0,3);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        delay(200);
                    }
                    else if((analogRead(Y_pin) < 250) && (density < 10)){
                        density++;
                        densityVar = map(density,1,10,10,1);
                        lcd.clear();
                        lcd.setCursor(0,3);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        delay(200);
                    }
                    if(digitalRead(SW_pin) == 0){
                        lcd.clear();
                        lcd.setCursor(0,1);
                        lcd.write(0);
                        lcd.setCursor(1,1);
                        lcd.print("Brightness: ");
                        lcd.print(bright);
                        lcd.setCursor(1,3);
                        lcd.print("Density: 1/");
                        lcd.print(densityVar);
                        bvd = 1;      
                        delay(150);               
                    }
                    if(analogRead(X_pin) < 250){
                        lcd.clear();
                        lcd.setCursor(0,3); 
                        lcd.write(0);
                        lcd.setCursor(2,0);
                        lcd.print("Snake");
                        lcd.setCursor(2,1);  
                        lcd.print("One-by-One");
                        lcd.setCursor(2,2);  
                        lcd.print("");
                        lcd.setCursor(2,3);  
                        lcd.print("Brightness");
                        bvd = 0;
                        menu = 0;
                        delay(150);
                    }
                }
            }
        break;
        case 9:                                   //Fading Color Speed
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("");
                lcd.setCursor(2,1);  
                lcd.print("Brightness");
                lcd.setCursor(2,2);  
                lcd.print("Fading Speed");
                lcd.setCursor(2,3);  
                lcd.print("Snake Speed");
                option++;
                delay(150);          
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Snake");
                lcd.setCursor(2,1);  
                lcd.print("One-by-One");
                lcd.setCursor(2,2);  
                lcd.print("");
                lcd.setCursor(2,3);  
                lcd.print("Brightness");
                option--;
                delay(350);
            }
            if(analogRead(X_pin) > 750){      //Into Submenu
                lcd.clear();
                lcd.setCursor(1,1);
                lcd.print("Speed: ");
                lcd.print(sped);
                menu = 3;
            }
            while(menu == 3){
                sleepFunction();
                if((analogRead(Y_pin) > 750) && (sped > 1)){      //Down (- Speed)
                    sped--;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Speed: ");
                    lcd.print(sped);
                    delay(200);
                }
                else if((analogRead(Y_pin) < 250) && (sped < 10)){      //Up (+ Speed)
                    sped++;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Speed: ");
                    lcd.print(sped);
                    delay(200);
                }
                if(analogRead(X_pin) < 250){      //Back Out
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("Snake");
                    lcd.setCursor(2,1);  
                    lcd.print("");
                    lcd.setCursor(2,2);  
                    lcd.print("Brightness");
                    lcd.setCursor(2,3);  
                    lcd.print("Fading Speed");
                    menu = 0;
                    spedVal = 330 - (30 * sped);
                    delay(150); 
                }
            }
        break;
        case 10:                                   //Snake Speed
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Brightness");
                lcd.setCursor(2,1);  
                lcd.print("Fading Speed");
                lcd.setCursor(2,2);  
                lcd.print("Snake Speed");
                lcd.setCursor(2,3);  
                lcd.print("Sleep Timer");
                option++;
                delay(150);          
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("One-by-One");
                lcd.setCursor(2,1);  
                lcd.print("");
                lcd.setCursor(2,2);  
                lcd.print("Brightness");
                lcd.setCursor(2,3);  
                lcd.print("Fading Speed");
                option--;
                delay(350);
            }
            if(analogRead(X_pin) > 750){      //Into Submenu
                lcd.clear();
                lcd.setCursor(1,1);
                lcd.print("Snake Speed: ");
                lcd.print(ssped);
                menu = 10;
            }
            while(menu == 10){
                sleepFunction();
                if((analogRead(Y_pin) > 750) && (ssped > 1)){      //Down (- Speed)
                    ssped--;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Snake Speed: ");
                    lcd.print(ssped);
                    delay(200);
                }
                else if((analogRead(Y_pin) < 250) && (ssped < 10)){      //Up (+ Speed)
                    ssped++;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Snake Speed: ");
                    lcd.print(ssped);
                    delay(200);
                }
                if(analogRead(X_pin) < 250){      //Back Out
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("");
                    lcd.setCursor(2,1);  
                    lcd.print("Brightness");
                    lcd.setCursor(2,2);  
                    lcd.print("Fading Speed");
                    lcd.setCursor(2,3);  
                    lcd.print("Snake Speed");
                    menu = 0;
                    delay(150); 
                }
            }
        break;
        case 11:                                   //Sleep Timer
            if(analogRead(Y_pin) > 750){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Fading Speed");
                lcd.setCursor(2,1);  
                lcd.print("Snake Speed");
                lcd.setCursor(2,2);  
                lcd.print("Sleep Timer");
                lcd.setCursor(2,3);  
                lcd.print("Toggle Screen");
                option++;
                delay(150);          
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("");
                lcd.setCursor(2,1);  
                lcd.print("Brightness");
                lcd.setCursor(2,2);  
                lcd.print("Fading Speed");
                lcd.setCursor(2,3);  
                lcd.print("Snake Speed");
                option--;
                delay(350);
            }
            if(analogRead(X_pin) > 750){      //Into Submenu
                lcd.clear();
                lcd.setCursor(1,1);
                lcd.print("Sleep Timer: ");
                lcd.print(sleep);
                lcd.print("hrs");
                menu = 9;
            }
            while(menu == 9){
                sleepFunction();
                if((analogRead(Y_pin) > 750) && (sleep > 1)){      //Down (- hr)
                    sleep--;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Sleep Timer: ");
                    lcd.print(sleep);
                    lcd.print("hrs");
                    delay(200);
                }
                else if((analogRead(Y_pin) < 250) && (sleep < 10)){      //Up (+ hr)
                    sleep++;
                    lcd.clear();
                    lcd.setCursor(1,1);
                    lcd.print("Sleep Timer: ");
                    lcd.print(sleep);
                    lcd.print("hrs");
                    delay(200);
                }
                if(analogRead(X_pin) < 250){      //Back Out
                    lcd.clear();
                    lcd.setCursor(0,3); 
                    lcd.write(0);
                    lcd.setCursor(2,0);
                    lcd.print("Brightness");
                    lcd.setCursor(2,1);  
                    lcd.print("Fading Speed");
                    lcd.setCursor(2,2);  
                    lcd.print("Snake Speed");
                    lcd.setCursor(2,3);  
                    lcd.print("Sleep Timer");
                    menu = 0;
                    sleepTime = sleep * 3600000;
                    currentTimeHolder = millis();
                    targetTime = currentTimeHolder + sleepTime;   //Setting target time
                    delay(150); 
                }
            }
        break;
        case 12:
            if(analogRead(Y_pin) > 750){
                //Nothing bc at bottom of menu          
            }
            else if(analogRead(Y_pin) < 250){
                lcd.clear();
                lcd.setCursor(0,3); 
                lcd.write(0);
                lcd.setCursor(2,0);
                lcd.print("Brightness");
                lcd.setCursor(2,1);  
                lcd.print("Fading Speed");
                lcd.setCursor(2,2);  
                lcd.print("Snake Speed");
                lcd.setCursor(2,3);  
                lcd.print("Sleep Timer");
                option--;
                delay(350);
            }
            if(screenLock == false){
                if(digitalRead(SW_pin) == 0){
                    lcd.setBacklight(LOW);
                    screenLock = true;
                    delay(350);
                }
            }
            else if(screenLock == true){
                if(digitalRead(SW_pin) == 0){
                    lcd.setBacklight(HIGH);
                    screenLock = false;
                    delay(350);
                }
            }
        break;
    } //Switch Statement Close

  
} //Loop Close

//Methods

void sleepFunction(){
    //Sleep Timer
    currentTime = millis();   //Setting current time 
    if(currentTime >= targetTime){
        menu = 0;
        option = 1;
        optionColor = 0;
        lcd.clear();
        lcd.setCursor(0,1); 
        lcd.write(0);
        lcd.setCursor(3,0);
        lcd.print("Choose Setting:");
        lcd.setCursor(2,1);  
        lcd.print("Solid Color");
        lcd.setCursor(2,2);  
        lcd.print("Fading Colors");
        lcd.setCursor(2,3);  
        lcd.print("Sync to Music");
        fill_solid(leds, NUM_LEDS, CHSV(0,0,0));  //Black
        FastLED.show();
        lcd.setBacklight(LOW);
        targetTime += sleepTime;    //Adds another time interval so you can wake it back up
    }
}

void nextPattern()   //Party
{
  // add one to the current pattern number, and wrap around at the end
  gCurrentPatternNumber = (gCurrentPatternNumber + 1) % ARRAY_SIZE( gPatterns);
}

void rainbow() //Rainbow
{
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, partyHue, 7);
}

void rainbowWithGlitter() //Not used
{
  // built-in FastLED rainbow, plus some random sparkly glitter
  rainbow();
  addGlitter(80);
}

void addGlitter( fract8 chanceOfGlitter) 
{
  if( random8() < chanceOfGlitter) {
    leds[ random16(NUM_LEDS) ] += CRGB::White;
  }
}

void confetti()     //Party
{
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 2);    //2 represents how long it takes for the color to fade away (makes it seem like there are more leds lighting up)
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( partyHue + random8(8), random8(180,255), 255);       //  leds[pos] += CHSV( partyHue + random8(64), 200, 255);   this was the original
}

void sinelon()   //Snake
{
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, 20);
  int pos = beatsin16( 13, 0, NUM_LEDS-1 );
  leds[pos] += CHSV( partyHue, 255, 192);
}

void bpm()    //Not Used
{
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(palette, partyHue+(i*2), beat-partyHue+(i*10));
  }
}

void juggle() {   //Not Used
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, 20);
  byte dothue = 0;
  for( int i = 0; i < 8; i++) {
    leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
}
