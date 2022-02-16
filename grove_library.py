from nanpy import (ArduinoApi, SerialManager, Tone)
from nanpy.rgb_lcd import rgb_lcd
from nanpy.grove_ultrasonic import Ultrasonic
from nanpy.chainableled import ChainableLED
from nanpy.servo import Servo
#from nanpy.led_bar import led_bar
#from nanpy.Grove_LED_Bar import Grove_LED_Bar
from time import sleep
import math

#import logging
#logging.basicConfig(level=logging.DEBUG)

####
## Arduino-related functions

# This function is used to initialize the Arduino and serial connection
def arduinoInit(deviceString):
    '''
    Parameter deviceString is the serial port to use
    eg. arduinoInit('COM96')
    or arduinoInit(0) to use default

    Return connection is the serial connection that can be used
    by other parts of code (see below)
    '''    
    global a
    global connection
    if (deviceString == 0):
        connection = SerialManager()
    else:
        connection = SerialManager(device=deviceString)
    a = ArduinoApi(connection=connection)
    return connection

# This function is used to read analog input on pin
def arduinoAnalogRead(pin):
    return a.analogRead(pin + 14)

# This function is used to write to analog device at pin
def arduinoAnalogWrite(pin, value):
    a.analogWrite(pin + 14, value)

# This function is used to read digital input on pin
def arduinoDigitalRead(pin):
    return a.digitalRead(pin)

# This function is used to write to digital device at pin
def arduinoDigitalWrite(pin, value):
    a.digitalWrite(pin, value)

####
## LCD-related functions

# This function is to initialize the LCD screen
def lcdInit(connection):
    '''
    Parameter connection is a serial connection created when arduinoInit()
    is called
    '''
    global lcd
    lcd = rgb_lcd(connection)
    lcd.setRGB(200, 100, 100)

# This function prints string msg to the LCD screen
def lcdPrintString(msg):
    lcd.printString(msg)

# This function prints integer n to the LCD screen
def lcdPrintInt(n):
    lcd.print(n)

# This function changes the background colour of the LCD screen
def lcdSetBackground(r, g, b):
    '''
    Paramaters r, g, b represent (red, green, blue) colour values
    '''
    lcd.setRGB(r, g, b)

# This function clears what is printed on the LCD screen
def lcdClear():
    lcd.clear()

# This function sets just the hue of the screen
def lcdSetHue(hue):
    h = float(hue)
    s = float(1)
    v = float(0.5)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    lcd.setRGB(r, g, b)

####
## Ultrasonic ranger related functions

# This function is to initialize the ultrasonic ranger
def ultraInit(pin, connection):
    '''
    Parameter pin indicates which digital pin the ultrasonic ranger is plugged
    Parameter connection is a serial connection created when arduinoInit()
    is called
    '''
    global sensor
    sensor = Ultrasonic(pin, connection=connection)
    return sensor

# This function returns the distance reading in cm
def ultraGetDistance():
    return sensor.MeasureInCentimeters()

####
## Chainable LED related functions

# This function is to initialize the chain of LEDs
def chainLEDInit(pin, count, connection):
    '''
    Parameter pin indicates which digital pin the LEDs are connected to
    Parameter count iInndicates how many we have connected
    Parameter connection is a serial connection created when arduinoInit()
    is called
    '''
    global leds
    leds = ChainableLED(pin, count, connection=connection)
    return leds

# This function returns the distance reading in cm
def chainLEDSetColour(index, red, blue, green):
    leds.setRGB(index, red, blue, green)

####
## Speaker related functions

# This function is to initialize the speaker
def speakerInit(pin, connection):
    '''
    Parameter pin indicates which digital pin the speaker is plugged
    Parameter connection is a serial connection created when arduinoInit()
    is called
    '''
    global tone
    tone = Tone(pin+1, connection=connection)
    return tone

# This function is to play a specific frequency for a set amount of time   
def speakerPlayNote(pin, frequency, duration):
    arduinoDigitalWrite(pin, 0)
    tone.play(frequency, duration)
    sleep(duration)
    arduinoDigitalWrite(pin, 1)
	

####
## Temperature sensor related functions

# This function returns a temperature in Celsius based on the analog sensor
# reading of pin
def tempGetCelsius(pin):
    '''
    Parameter pin indicates which analog pin the speaker is plugged
    '''
    reading = float(a.analogRead(pin + 14))
    R = 1023.0/reading-1.0
    R = 100000*R
    temperature = 1.0/(math.log10(R/100000)/4275+1/298.15)-273.15;
    return temperature
    
####
## Servo motor related functions

# This function is to initialize the servo
def servoInit(pin):
    '''
    Parameter pin indicates which digital pin the servo is plugged
    '''
    global servo
    servo = Servo(pin, connection)
    return servo

# This function is to move the servo to angle
def servoMove(angle):
    '''
    Parameter angle indicates angle in degrees
    '''
    servo.write(angle)
    sleep(0.5)

####
## LED Bar related functions

# This function is to initialize the LED bar
def barInit(pin):
    '''
    Parameter pin indicates which digital pin the servo is plugged
    '''
    global bar
    bar = Grove_LED_Bar(pin, connection)
    return bar

# This function is to light all bars up to level
def barSetLevel(level):
    '''
    Parameter level, 0 <= level <=10
    '''
    bar.setLevel(level)
    sleep(0.5)
