__author__ = 'Kaike'

from sqlite3 import dbapi2 as sqlite3

class DatabaseService(object):
    DATABASE = 'database.db'


    def get_db(self):
        return sqlite3.connect(self.DATABASE)

    def saveState(self, houseState):
        db = self.get_db()
        if db is None:
            return False

        for user in houseState.users:
            db.execute('insert into houseStates (room, user , light, temperature, hour) values (?, ?, ?, ?, ?)', [
            houseState.room, user, houseState.light, houseState.temperature, houseState.hour
            ])
            db.commit()
        return True


    def saveHouseStateRules(self, houseStateRules):
        db = self.get_db()
        if db is None:
            return False

        for houseStateRule in houseStateRules:
            for user in houseStateRule.users:
                db.execute('insert into houseStateRules (room, user , light, temperature, hour) values (?, ?, ?, ?, ?)', [
                houseStateRule.room, user, houseStateRule.light, houseStateRule.temperature, houseStateRule.hour
                ])
                db.commit()
        return True

    def getHouseStates(self):
        db = self.get_db()
        if db is None:
            return False
        cur = db.execute('select room, user, light, temperature, hour from houseStates order by db_id')
        return self.parseQueryResultToList(cur.fetchall())

    def getHouseStateRules(self):
        db = self.get_db()
        if db is None:
            return False
        cur = db.execute('select room, user, light, temperature, hour from houseStateRules order by db_id')
        return self.parseQueryResultToList(cur.fetchall())

    def parseQueryResultToList(resultFromDb):
        result = list()
        for row in resultFromDb:
            currentRow = {}
            currentRow["room"] = row[0]
            currentRow["user"] = row[1]
            currentRow["light"] = row[2]
            currentRow["temperature"] = row[3]
            currentRow["hour"] = row[4]
            result.append(currentRow)
        return result