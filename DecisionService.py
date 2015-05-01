__author__ = 'Kaike'

import HouseStateManager
import HouseStateRulesManager
import DevicesControl

class DecisionService(object):
    def __init__(self):
        self.houseStateRulesManager = HouseStateRulesManager()
        self.houseStateManager = HouseStateManager()
        self.devicesControl = DevicesControl()

    def makeDecision(self):
        rules = self.houseStateRulesManager.getHouseStateRules()
        currentState = self.houseStateManager.getCurrentHouseState()

        targetRule = {}
        #for rule in rules:
        #    if rule.room == currentState.room and rule.hour == currentState.hour
        #        for user in rule.users:

