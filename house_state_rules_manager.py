__author__ = 'Kaike'
#from sklearn import svm
#from Model import HouseState

from Model.room_state import RoomStateRule
import database_service
import pickle
import os
from sklearn import tree

class HouseStateRulesManager(object):
    def __init__(self):
        self.databaseService = database_service.DatabaseService()

    def create_rules(self):
        history = self.databaseService.get_house_states()

        roomNames = ["office", "bedroom"]
        for roomName in roomNames:
            devices = ["light","temperature","curtain"]
            for device in devices:
                deviceName = roomName + device
                roomIndex = 0 if roomName == "office" else 1
                roomHistory = history[history['room'] == roomIndex]
                treeResult = tree.DecisionTreeClassifier(criterion="entropy", max_depth = 20)
                treeResult.fit(roomHistory.filter(regex= 'user|room|hour').values, roomHistory.filter(regex= device).values)
                with open(deviceName + '.plk', 'wb') as f:
                    pickle.dump(treeResult, f)
                self.export_decision_tree_to_PDF(treeResult, deviceName, device)

    def get_room_rule_to_apply(self, roomState):
        roomName = "office" if roomState.room == 0 else "bedroom"
        decisionTreeEntries = [roomState.users[0],roomState.room, roomState.hour]
        roomStateRuleResult = RoomStateRule(0,0,0,0,0,0)
        
        with open(roomName + "light" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.light = decisionTree.predict(decisionTreeEntries)[0]
            f.close()

        with open(roomName + "temperature" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.temperature = decisionTree.predict(decisionTreeEntries)[0]
            f.close()
            
        with open(roomName + "curtain" + '.plk', 'rb') as f:
            decisionTree = pickle.load(f)
            roomStateRuleResult.curtain = decisionTree.predict(decisionTreeEntries)[0]
            f.close()
            
        roomStateRuleResult.hour = roomState.hour
        roomStateRuleResult.user = roomState.users[0]
        roomStateRuleResult.room = roomState.room
        
        return roomStateRuleResult

    def export_decision_tree_to_PDF(self, decisionTree, treeName, targetedVariableNameFromTree):
        fileName = treeName + '.dot'
        with open(fileName,'w') as f:
            f = tree.export_graphviz(decisionTree, out_file = f, feature_names = ['usuario','comodo','hora',targetedVariableNameFromTree])

        os.system("dot -Tpdf " + fileName + " -o " + treeName + ".pdf")
        os.unlink(fileName)











