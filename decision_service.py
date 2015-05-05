__author__ = 'Kaike'

import house_state_manager
import house_state_rules_manager
import devices_control

class DecisionService(object):
    def __init__(self):
        self.houseStateRulesManager = house_state_rules_manager.HouseStateRulesManager()
        self.houseStateManager = house_state_manager.HouseStateManager()
        self.devicesControl = devices_control.DevicesControl()


    def make_decision(self,  roomState):
        roomName = "bedroom" if roomState.room == 0 else "office"

        actual_state = self.houseStateManager.get_current_bedroom_state() if roomState.room == 0 else self.houseStateManager.get_current_bedroom_state()
        rule_to_apply = self.houseStateRulesManager.get_room_rule_to_apply(roomState)

        if(rule_to_apply.curtain == actual_state.curtain):
            self.devicesControl.change_device(rule_to_apply.curtain, "curtain", roomName)

        if (rule_to_apply.light == actual_state.light):
            self.devicesControl.change_device(rule_to_apply.light, "light", roomName)

        if (rule_to_apply.temperature == actual_state.temperature):
            self.devicesControl.change_device(rule_to_apply.temperature, "light", roomName)

