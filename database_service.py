__author__ = 'Kaike'

from sqlite3 import dbapi2 as sqlite3
from pandas import *


class DatabaseService(object):
    DATABASE = 'database.db'

    def get_db(self):
        return sqlite3.connect(self.DATABASE)

    def save_house_state(self, houseState):
        db = self.get_db()
        if db is None:
            return False
        for user in houseState.users:
            db.execute('insert into houseStates (room, userName , light, temperature, hourOfDay, curtain) values (?, ?, ?, ?, ?)', [
            houseState.room, user, houseState.light, houseState.temperature, houseState.hour, houseState.curtain
            ])
            db.commit()
        return True

    def get_house_states(self):
        db = self.get_db()
        if db is None:
            return False
        cur = db.execute('select room, userName, light, temperature, hourOfDay, curtain from houseStates order by db_id')
        return self.__parse_query_result_to_data_frame(cur.fetchall())

    def __parse_query_result_to_data_frame(self, resultFromDb):
        result = list()
        for row in resultFromDb:
            currentRow = {}
            currentRow["room"] = row[0]
            currentRow["userName"] = row[1]
            currentRow["light"] = row[2]
            currentRow["temperature"] = row[3]
            currentRow["hourOfDay"] = row[4]
            currentRow["curtain"] = row[5]
            result.append(currentRow)

        rowsList = []
        for row in result:
            rowsList.append([row['userName'], row['room'], row['hourOfDay'], row['light'], row['temperature'], row['curtain']])

        return DataFrame(rowsList, columns=['user', 'room', 'hour', 'light', 'temperature', 'curtain'])
