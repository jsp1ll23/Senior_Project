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
    os.system("echo '" + message + "' |pdsend 3000 localhost udp")

def send2Pd2(message=' '):
    os.system("echo '" + message + "' |pdsend 2900 localhost udp")

def send2Pd3(message=' '):
    os.system("echo '" + message + "' |pdsend 2800 localhost udp")

def send2Pd4(message=' '):
    os.system("echo '" + message + "' |pdsend 2700 localhost udp")

def AudioOff():
    message = '0 0;'
    send2Pd1(message)

def AudioOn():
    message = '0 1;'
    send2Pd1(message)

def setMix1(mix1):
    message = '0 ' + str(mix1) + ';'
    send2Pd2(message)

def setMix2(mix2):
    message = '0 ' + str(mix2) + ';'
    send2Pd3(message)

def ClosePd():
    message = '0 1;'
    send2Pd4(message)

def RunEffect(x):
    subprocess.Popen(['nohup', 'pd', x + '.pd'],
                 stdout=open('/dev/null', 'w'),
                 stderr=open('logfil.log', 'a'),
                 preexec_fn=os.setpgrp)
    
def StopEffect():
    os.system('pkill pd')

    
def getmix1_distortion(x):
    value = (x/2048)*4
    return value

def getmix2_distortion(x):
    value = (x/2048)*25
    return value

lcd.clear()

lcd.message('Please Wait...')

#Initially open Clean effect
Filename = 'Clean'
RunEffect(Filename)

time.sleep(1)
lcd.clear()
lcd.message(Filename)
Old_Filename = 'Clean'

while True:
    values = [0]*3
    for i in range(3):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    Selector = values[0]
    Mix1_ADC = values[1]
    Mix2_ADC = values[2]
    Mix2 = getmix2_distortion(float(Mix2_ADC))
    Mix1 = getmix1_distortion(float(Mix1_ADC))
    if(Selector > 1024):
        Filrename = 'Clean'
    else:
        Filename = 'Distortion'
    if(Old_Filename != Filename):
        os.system('pkill pd')
        lcd.clear()
        RunEffect(Filename)
        lcd.message(Filename)
    AudioOn()
    time.sleep(.2)
    setMix1(Mix1)
    time.sleep(.2)
    setMix2(Mix2)
    time.sleep(.2)
    Old_Filename = Filename
