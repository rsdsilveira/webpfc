__author__ = 'Kaike'
class HouseStateRulesManager(object):
    def __init__(self, databaseService):
        self.databaseService = databaseService

    def createRules(self):
        rules = self.databaseService.getHouseStates()
        self.databaseService.saveHouseStateRules(self.newRulesAlgotithm())

    def newRulesAlgotithm(self, history):
        return list()

    def getHouseStateRules(self):
        return self.databaseService.getHouseStateRules()