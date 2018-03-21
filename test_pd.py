import os
import time

def send2Pd1(message=' '):
    os.system("echo '" + message + "' |pdsend 3000")

def send2Pd2(message=' '):
    os.system("echo '" + message + "' |pdsend 2900")

def send2Pd3(message=' '):
    os.system("echo '" + message + "' |pdsend 2800")

def send2Pd4(message=' '):
    os.system("echo '" + message + "' |pdsend 2700")

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

AudioOn()
time.sleep(.2)
setMix1(0)
time.sleep(.2)
setMix2(25)
time.sleep(.2)
ClosePd()
