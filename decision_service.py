__author__ = 'Kaike'

import house_state_manager
import house_state_rules_manager
import devices_control

class DecisionService(object):
    def __init__(self):
        self.houseStateRulesManager = house_state_rules_manager.HouseStateRulesManager()
        self.houseStateManager = house_state_manager.HouseStateManager()


    def make_decision(self,  roomState):
        roomName = "office" if roomState.room == 0 else "bedroom"

        actual_state = self.houseStateManager.get_current_office_state() if roomName == "office" else self.houseStateManager.get_current_bedroom_state()
        rule_to_apply = self.houseStateRulesManager.get_room_rule_to_apply(roomState)

        if(rule_to_apply.curtain != actual_state.curtain):
            print roomName + " " + "curtain: " + "de " + str(actual_state.curtain) + " para "
            str(rule_to_apply.curtain)
            if(roomName == "bedroom"):
                self.houseStateManager.change_bedroom_curtain(rule_to_apply.curtain)
            else:
                self.houseStateManager.change_office_curtain(rule_to_apply.curtain)

        if (rule_to_apply.light != actual_state.light):
            print roomName + " " + "light: " + "de " + str(actual_state.light) + " para "
            str(rule_to_apply.light)
            if (roomName == "bedroom"):
                self.houseStateManager.change_bedroom_light(rule_to_apply.light)
            else:
                self.houseStateManager.change_office_light(rule_to_apply.light)


        if (rule_to_apply.temperature != actual_state.temperature):
            print roomName + " " + "temperature: " + "de " + str(actual_state.temperature) + " para "
            str(rule_to_apply.temperature)
            if (roomName == "bedroom"):
                self.houseStateManager.change_bedroom_temperature(rule_to_apply.temperature)
            else:
                self.houseStateManager.change_office_temperature(rule_to_apply.temperature)


