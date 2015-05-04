__author__ = 'Kaike'

import house_state_manager
import house_state_rules_manager
import devices_control

class DecisionService(object):
    def __init__(self):
        self.houseStateRulesManager = house_state_rules_manager.HouseStateRulesManager()
        self.houseStateManager = house_state_manager.HouseStateManager()
        self.devicesControl = devices_control.DevicesControl()

    def makeDecision(self,  house_state=None):
        rules = self.houseStateRulesManager.getHouseStateRules()
        actual_state = {}
        if house_state.room == 0:
            actual_state = self.houseStateManager.get_current_office_state()
        if house_state.room == 1:
            actual_state = self.houseStateManager.get_current_bedroom_state()

        targetRule = {}
#        for rule in rules:
#            if rule.room == actual_state.room and rule.hour == actual_state.hour
#                for user in rule.users:

