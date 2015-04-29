__author__ = 'Kaike'
import DatabaseService
from Model import HouseState
from werkzeug.contrib.cache import SimpleCache
import datetime

class HouseStateManager (object):
    def __init__(self):
        self.databaseService = DatabaseService()
        self.save_current_house_state(HouseState(0, self.format_time(datetime.time.now()), 0, 0, 0, 0))
        self.save_current_house_state(HouseState(1, self.format_time(datetime.time.now()), 0, 0, 0, 0))

    def save_current_house_state(self, houseState):
        SimpleCache().set("current_house_state", houseState)

    def save_current_office_state(self, houseState):
        SimpleCache().set("current_office_state", houseState)

    def save_current_bedroom_state(self, houseState):
        SimpleCache().set("current_bedroom_state", houseState)

    def get_current_house_state(self):
        return SimpleCache().get("current_house_state")

    def get_current_office_state(self):
        return SimpleCache().get("current_office_state")

    def get_current_bedroom_state(self):
        return SimpleCache().get("current_bedroom_state")

    def save_house_state_in_db(self, houseState):
        self.databaseService.save_house_state(houseState)


    #def format_time(self, time):
    #    time.hour = datetime.datetime.now().hour
    #    if datetime.datetime.now().minute > 30:
    #        time.minute = 30
    #    else:
    #        time.minute = 0
    #    time.second = 0
    #
    #    datetime.datetime.now().time()
    #    return time

    def change_temperature(self, new_temperature):
        self.temperature = new_temperature

    def change_light(self, new_light):
        self.light = new_light

    def change_curtain(self, new_curtain):
        self.curtain = new_curtain