#ENG 1020 LAB PROJECT#
"""
Assumes that the sound sensor takes input as sound intensity
        that the button will be pressed to end the main loop

Returns the list of values created by the sound sensor in the form of frequencies from the speaker
        A graph showing the values from that list vs the index of each individual element
        A descending C major scale to let the user know the program has ended

"""

#First we need to import all the necesssary libraires for our program to run.
from grove_library import *
import math
import matplotlib.pyplot as plt
from time import sleep

#Next we have to initialize the arduino, the button and the speaker.
connection = arduinoInit(0)
bpressed = arduinoDigitalRead(7)
speaker = speakerInit(4, 0)

#Because we want the sound sensor to monitor the sound level, we need to store these values in a list.
soundlvllist = list()

#Main loop used for the sound sensor to monitor sound level. The list will be appended with each new reading from the sound sensor.
while True:
    sound = arduinoAnalogRead(0)
    soundlvlist = soundlvllist.append(sound)
    
#nested loop used for the speaker to play the list of tones created from the input of the sound sensor
    for i in soundlvllist:
        speakerPlayNote(4, i, 1)
        
    #condition statements are used for the button to break the loop when it is pressed or to continue the loop when the button is not pressed. Once pressed, it will print a graph of the frequency of the speaker vs the index of the list.
    if bpressed == True:
        bpressed = arduinoDigitalRead(7)
        plt.plot(soundlvllist)
        plt.xlabel('Index')
        plt.ylabel('Frequency(Hz)')
        plt.show()
        soundlvllist = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63]
        #speaker will play a certain audio to let user know the program has ended.
        for i in soundlvllist:
            speakerPlayNote(4, i, 0.30)
        break
    elif bpressed == False:
        bpressed = arduinoDigitalRead(7)
