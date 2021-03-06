__author__ = 'Kaike'
import database_service
import devices_control
from Model import room_state
from werkzeug.contrib.cache import SimpleCache
import datetime

class HouseStateManager (object):
    def __init__(self):
        self.sc = SimpleCache()
        self.databaseService = database_service.DatabaseService()
        self.devicesControl = devices_control.DevicesControl()
        self.save_current_office_state(room_state.RoomState(0, self.format_current_time(), [], 0, 0, 0))
        self.save_current_bedroom_state(room_state.RoomState(1, self.format_current_time(), [], 0, 0, 0))
        print self.sc.get("current_office_state")

    def save_current_office_state(self, houseState):
        houseState.hour = self.format_current_time()
        self.sc.set("current_office_state", houseState)

    def save_current_bedroom_state(self, houseState):
        houseState.hour = self.format_current_time()
        self.sc.set("current_bedroom_state", houseState)

    def get_current_house_state(self):
        return self.sc.get("current_house_state")

    def get_current_office_state(self):
        return self.sc.get("current_office_state")

    def get_current_bedroom_state(self):
        return self.sc.get("current_bedroom_state")

    def save_house_state_in_db(self, houseState):
        houseState.hour = self.format_current_time()
        self.databaseService.save_house_state(houseState)


    def format_current_time(self):
        formatted_time = float(datetime.datetime.now().hour)
        if datetime.datetime.now().minute > 30:
            formatted_time = formatted_time + 0.5
        return formatted_time

    def change_office_temperature(self, new_temperature):
        office_state = self.get_current_office_state()
        office_state.temperature = new_temperature
        self.save_current_office_state(office_state)
        self.devicesControl.change_device(new_temperature,"temperature","office")

    def change_bedroom_temperature(self, new_temperature):
        bedroom_state = self.get_current_bedroom_state()
        bedroom_state.temperature = new_temperature
        self.save_current_bedroom_state(bedroom_state)
        self.devicesControl.change_device(new_temperature,"temperature", "bedroom")


    def change_office_light(self, new_light):
        office_state = self.get_current_office_state()
        office_state.light = new_light
        self.save_current_office_state(office_state)
        self.devicesControl.change_device(new_light,"light","bedroom")

    def change_bedroom_light(self, new_light):
        bedroom_state = self.get_current_bedroom_state()
        bedroom_state.light = new_light
        self.save_current_bedroom_state(bedroom_state)
        self.devicesControl.change_device(new_light, "light","bedroom")

    def change_office_curtain(self, new_curtain):
        office_state = self.get_current_office_state()
        office_state.curtain = new_curtain
        self.save_current_office_state(office_state)
        self.devicesControl.change_device(new_curtain, "curtain","office")

    def change_bedroom_curtain(self, new_curtain):
        bedroom_state = self.get_current_bedroom_state()
        bedroom_state.curtain = new_curtain
        self.save_current_bedroom_state(bedroom_state)
        self.devicesControl.change_device(new_curtain, "curtain", "bedroom")
