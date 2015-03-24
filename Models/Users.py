__author__ = 'Kaike'


from enum import Enum


class Users(Enum):
    default = 0
    rafael = 1
    cesar = 2
    carlos = 3

class User(object):
    def __init__(self, userNumber, actualRoom):
        self.number = userNumber
        self.room = actualRoom

