__author__ = 'Kaike'
#from sklearn import svm
#from Model import HouseState
import DatabaseService
import pickle
import pandas as PandasLibrary
from model import *
from sklearn import tree

class HouseStateRulesManager(object):
    def __init__(self):
        self.databaseService = DatabaseService()

    def create_rules(self):
        rules = self.databaseService.get_house_states()
        self.databaseService.save_house_state_rules(self.new_rules_algotithm())

    def new_rules_algotithm(self):
        history = self.databaseService.get_house_states()

        roomNames = ["office", "bedroom"]
        for roomName in roomNames:
            devices = ["Light","Temperature","Curtain"]
            for device in devices:
                deviceName = roomName + device
                treeResult = tree.DecisionTreeClassifier(criterion="entropy")
                treeResult.fit(history.filter(regex= 'user|room|hour'), history.filter(regex= deviceName))
                with open(deviceName + '.plk', 'wb') as f:
                    pickle.dump(treeResult, f)

    def getHouseStateRules(self, roomState):
        roomName = "office" if roomState.room == 0 else "bedroom"
        # na linha abaixo coloquei roomState.users[0], mas e se um roomState tem mais de um user?
        decisionTreeEntries = [roomState.users[0],roomState.room, roomState.hour]
        roomStateRuleResult = RoomStateRule()
        
        with open(roomName + "Light" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.light = decisionTree.Predict(decisionTreeEntries)[0]
            f.close()

        with open(roomName + "Temperature" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.temperature = decisionTree.Predict(decisionTreeEntries)[0]
            f.close()
            
        with open(roomName + "Curtain" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.curtain = decisionTree.Predict(decisionTreeEntries)[0]
            f.close()
            
        roomStateRuleResult.hour = roomState.hour
        # na linha abaixo coloquei roomState.users[0], mas e se um roomState tem mais de um user?
        roomStateRuleResult.user = roomState.users[0]
        roomStateRuleResult.room = roomState.room
        
        return roomStateRuleResult            
