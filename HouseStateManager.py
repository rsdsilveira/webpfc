__author__ = 'Kaike'

class HouseStateManager (object):
    def __init__(self, users):
        self.users = users
        self.light = 0
        self.temperature = 0

    def saveCurrentHouseState(self, houseState):
        SimpleCache().set("current_house_state", houseState)

    def getCurrentHouseState(self):
        return SimpleCache().get("current_house_state")

    def changeTemperature(self, newTemperature):
        self.temperature = newTemperature

    def changeLight(self, newLight):
        self.light = newLight

    def userChangeRoom(self, userNumber, room):
        for user in self.users:
            if(user.number == userNumber):
                user.room = room