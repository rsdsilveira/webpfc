__author__ = 'Kaike'
import datetime
import Models.HouseState

def EventHandler(object):
    def __init__(self, houseStateManager, decisionService)
        self.houseStateManager = houseStateManager
        self.decisionService = decisionService

    def userEvent(self, user, room):
        hour = self.getHour()
        houseState = Models.HouseState(room, hour, user, self.houseStateManager.light, self.houseStateManager.temperature)
        self.houseStateManager.saveCurrentHouseState(houseState)
        self.decisionService.makeDecision()

    def checkForDecisions(self):
        self.decisionService.makeDecision()

    def getHour(self):
        return datetime.datetime.now().time()


