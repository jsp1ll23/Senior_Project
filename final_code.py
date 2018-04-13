#!/usr/bin/env python
import os
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_CharLCD as LCD
import subprocess
import socket

# Raspberry Pi pin configuration:
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


#Setting up ADC pin configuration:
CLK  = 5
MISO = 6
MOSI = 13
CS   = 19
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#user definitions

def send2Pd1(message=' '):
    os.system("echo '" + message + "' |pdsend 3500")

def send2Pd2(message=' '):
    os.system("echo '" + message + "' |pdsend 3400")

def send2Pd3(message=' '):
    os.system("echo '" + message + "' |pdsend 3300")

def send2Pd4(message=' '):
    os.system("echo '" + message + "' |pdsend 3200")

def send2Pd5(message=' '):
    os.system("echo '" + message + "' |pdsend 3100")

def AudioOff():
    message = '0 0;'
    send2Pd2(message)

def AudioOn():
    message = '0 1;'
    send2Pd2(message)

def setMix1(mix1):
    message = '0 ' + str(mix1) + ';'
    send2Pd3(message)

def setMix2(mix2):
    message = '1 ' + str(mix2) + ';'
    send2Pd3(message)

def setMix3():
    message = '2 89;'
    send2Pd3(message)

def setroom(mix1):
    message = '0 ' + str(mix1) + ';'
    send2Pd5(message)

def setdamp(mix2):
    message = '1 ' + str(mix2) + ';'
    send2Pd5(message)

def setWet():
    message = '0 0.5;'
    send2Pd4(message)

def setDry():
    message = '1 0.5;'
    send2Pd4(message)

def Clean(x):
    message = '0 ' +str(x) + ';'
    send2Pd1(message)

def Distortion(x):
    message = '1 ' +str(x) + ';'
    send2Pd1(message)

def Reverb(x):
    message = '2 ' +str(x) + ';'
    send2Pd1(message)

def getmix1_distortion(x):
    value = (x/1023)*100
    return value

def getmix2_distortion(x):
    value = (x/1023)*1
    return value

def getmix_reverb(x):
    value = (x/1023)
    return value

Old_Filename = '0'
lcd.clear()
subprocess.Popen(['nohup', 'pd','/home/pi/final_pd.pd'],
            stdout=open('/dev/null', 'w'),
            stderr=open('logfil.log', 'a'),
            preexec_fn=os.setpgrp)

while True:
    values = [0]*3
    for i in range(3):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    Selector = values[2]
    Mix1_ADC = values[1]
    Mix2_ADC = values[0]
    if(Selector < 342 ):
        Filename = 'Clean'
        Mixname = '\nNon-edit'
        Mix1 = 0
        Mix2 = 0
        Reverb(0)
        Distortion(0)
        Clean(1)
    elif(Selector > 341 and Selector < 683):
        Filename = 'Distortion'
        Mixname = '\nHarshness, Vol'
        setMix1(getmix1_distortion(float(Mix1_ADC)))
        setMix2(getmix2_distortion(float(Mix2_ADC)))
        setMix3()
        Clean(0)
        Reverb(0)
        Distortion(1)
    else:
        Filename = 'Reverb'
        Mixname = '\nLength, Damping'
        setroom(getmix_reverb(float(Mix1_ADC)))
        setdamp(getmix_reverb(float(Mix2_ADC)))
        setWet()
        setDry()
        Clean(0)
        Distortion(0)
        Reverb(1)
    if(Old_Filename != Filename):
        lcd.clear()
        lcd.message(Filename)
        lcd.message(Mixname)
    AudioOn()
    Old_Filename = Filename
