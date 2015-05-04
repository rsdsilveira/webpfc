__author__ = 'Kaike'
#from sklearn import svm
#from Model import HouseState
import database_service

class HouseStateRulesManager(object):
    def __init__(self):
        self.databaseService = database_service.DatabaseService()

    def create_rules(self):
        rules = self.databaseService.get_house_states()
        self.databaseService.save_house_state_rules(self.new_rules_algotithm())

    def new_rules_algotithm(self, history):
        return list()

    def getHouseStateRules(self):
        return self.databaseService.getHouseStateRules()
