__author__ = 'Kaike'
#from sklearn import svm
#from Model import HouseState

from Model.room_state import RoomStateRule
import database_service
import pickle
import pandas as PandasLibrary
import os
from Model import *
from sklearn import tree

class HouseStateRulesManager(object):
    def __init__(self):
        self.databaseService = database_service.DatabaseService()

    def create_rules(self):
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
                self.export_decision_tree_to_PDF(treeResult, deviceName, device)

    def get_room_rule_to_apply(self, roomState):
        roomName = "office" if roomState.room == 0 else "bedroom"
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
        roomStateRuleResult.user = roomState.users[0]
        roomStateRuleResult.room = roomState.room
        
        return roomStateRuleResult

    def export_decision_tree_to_PDF(self, decisionTree, treeName, targetedVariableNameFromTree):
        fileName = treeName + '.dot'
        with open(fileName,'w') as f:
            f = decisionTree.export_graphviz(clf, out_file = f, feature_names = ['usuario','comodo','hora',targetedVariableNameFromTree])

        os.system("dot -Tpdf" + fileName + " -o " + treeName + ".pdf")
        os.unlink(fileName)











