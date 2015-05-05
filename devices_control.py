__author__ = 'Kaike'

import time
import serial

class DevicesControl(object):

    def __init__(self):
        return

    def change_device(self, value, deviceName, roomName):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend(deviceName, roomName, value)
        self.sendSerialMessage(port, serialMessage)
        return

    def __sendSerialMessage(self,port, messageArray):
        time.sleep(0.5)
        for charSerial in messageArray:
            port.write(charSerial)
            time.sleep(0.1)


    def __getSerialPort(self):
        port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = 3.0)
        if(port.isOpen() == False):
            port.open()

        port.flushInput()
        port.flushOutput()
        time.sleep(2)
        return port


    def __getSerialMessageToSend(self, deviceName, roomName, valueToChange):
        serialMessage = []
        if (roomName == "bedroom" and deviceName == "light"):
            serialMessage = [chr(3), chr(34), chr(0), chr(2), chr(13)] if valueToChange == 0 else [chr(3), chr(34), chr(0), chr(1), chr(13)]
        if (roomName == "bedroom" and deviceName == "temperature"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (roomName == "bedroom" and deviceName == "curtain"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (roomName == "office" and deviceName == "light"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (roomName == "office" and deviceName == "temperature"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (roomName == "office" and deviceName == "curtain"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]

        return serialMessage






