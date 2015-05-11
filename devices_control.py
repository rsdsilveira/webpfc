__author__ = 'Kaike'

import time
import serial
from Model import room_state

class DevicesControl(object):

    def __init__(self):
        return

    def change_device(self, value, deviceName, roomName):
        self.__port = self.__getSerialPort()
        serialMessage = self.__getSerialMessageToSend(deviceName, roomName, value)
        self.__sendSerialMessage(self.__port, serialMessage)
        return

    def get_device_state(self, deviceName, roomName):
        self.__port = self.__getSerialPort()
        messageToGetStates = [chr(2), chr(1), chr(1), chr(1), chr(13)]
        self.__sendSerialMessage(self.__port, messageToGetStates)

        data = self.__port.read(200)
        devicesArray = self.__transform_refresh_data_into_array(data)
        stateFromCircuit = 0
        deviceId = self.__get_device_id(deviceName, roomName)

        if(devicesArray[0][0] == deviceId):
            if(deviceId == 22 or deviceId == 26): # ar condicionado
                stateFromCircuit = devicesArray[0][1]
            else:
                stateFromCircuit = 0 if devicesArray[0][1] == 1 else 1
                
        return stateFromCircuit

    def __sendSerialMessage(self,port, messageArray):
        time.sleep(0.5)
        for charSerial in messageArray:
            port.write(charSerial)
            time.sleep(0.1)

    def __transform_refresh_data_into_array(self, data):
        devicesArray = list()
        if (len(data)) > 0:
            deviceState = list()
            for elem in data:
                elementParsed = ord(elem)
                if (elementParsed == 13):
                    devicesArray.append(deviceState)
                    deviceState = list()
                else:
                    deviceState.append(elementParsed)
        else:
            print ""

        return devicesArray

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

    def __get_device_id(self, deviceName, roomName):
        deviceId = 0
        if (roomName == "bedroom" and deviceName == "light"):
            deviceId = 1
        if (roomName == "bedroom" and deviceName == "temperature"):
            deviceId = 1
        if (roomName == "bedroom" and deviceName == "curtain"):
            deviceId = 1
        if (roomName == "office" and deviceName == "light"):
            deviceId = 1
        if (roomName == "office" and deviceName == "temperature"):
            deviceId = 1
        if (roomName == "office" and deviceName == "curtain"):
            deviceId = 1

        return deviceId

    def __getSerialPort(self):
        port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
        if (port.isOpen() == False):
            port.open()

        port.flushInput()
        port.flushOutput()
        time.sleep(3)
        return port
