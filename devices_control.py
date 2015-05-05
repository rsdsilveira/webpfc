__author__ = 'Kaike'

import time
import serial

class DevicesControl(object):

    def __init__(self):
        return

    def change_bedroom_temperature(self, value):
        port =  self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("bedroomTemperature",value)
        self.sendSerialMessage(port, serialMessage)
        return

    def change_bedroom_light(self, value):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("bedroomLight", value)
        self.sendSerialMessage(port, serialMessage)
        return

    def change_bedroom_curtain(self,value):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("bedroomCurtain", value)
        self.sendSerialMessage(port, serialMessage)
        return

    def change_office_temperature(self, value):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("officeTemperature", value)
        self.sendSerialMessage(port, serialMessage)
        return

    def change_office_light(self, value):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("officeLight", value)
        self.sendSerialMessage(port, serialMessage)
        return

    def change_office_curtain(self, value):
        port = self.getSerialPort()
        serialMessage = self.getSerialMessageToSend("officeCurtain", value)
        self.sendSerialMessage(port, serialMessage)
        return

    def sendSerialMessage(self,port, messageArray):
        time.sleep(0.5)
        for charSerial in messageArray:
            port.write(charSerial)
            time.sleep(0.1)


    def getSerialPort(self):
        port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = 3.0)
        if(port.isOpen() == False):
            port.open()

        port.flushInput()
        port.flushOutput()
        time.sleep(2)
        return port


    def getSerialMessageToSend(self, deviceName, valueToChange):
        serialMessage = []
        if (deviceName == "bedroomLight"):
            serialMessage = [chr(3), chr(34), chr(0), chr(2), chr(13)] if valueToChange == 0 else [chr(3), chr(34), chr(0), chr(1), chr(13)]
        if (deviceName == "bedroomCurtain"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (deviceName == "bedroomTemperature"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (deviceName == "officeLight"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (deviceName == "officeCurtain"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]
        if (deviceName == "officeTemperature"):
            serialMessage = [chr(), chr(), chr(), chr(), chr()]

        return serialMessage






