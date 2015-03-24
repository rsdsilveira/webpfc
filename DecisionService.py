__author__ = 'Kaike'

class DecisionService(object):
    def __init__(self, houseStateRulesManager, houseStateManager):
        self.houseStateRulesManager = houseStateRulesManager
        self.houseStateManager = houseStateManager

    def makeDecision(self):
        rules = self.houseStateRulesManager.getHouseStateRules()
        currentState = self.houseStateManager.getCurrentHouseState()

        targetRule = {}
        #for rule in rules:
        #    if rule.room == currentState.room and rule.hour == currentState.hour
        #        for user in rule.users:

