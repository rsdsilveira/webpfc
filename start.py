####### ------------------------ IMPORTS ----------------------------- #######

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response
from werkzeug.contrib.cache import SimpleCache

import house_state_manager
#from HouseStateManager import HouseStateManager
#from house_state_manager import HouseStateManager
import decision_service
import devices_control
from Model.room_state import RoomState
import datetime

####### ------------------ APP START CONFIGURATION -------------------- #######

DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)



####### --------------------init---------------------------------------######



houseStateManager = house_state_manager.HouseStateManager()
decisionService = decision_service.DecisionService()
devicesControl = devices_control.DevicesControl()

####### ------------------------ DATABASE ----------------------------- #######

def get_db():
    return sqlite3.connect(DATABASE)

def init_db():
    db = get_db()
    if db is None:
        return 'Nao ha conexao com o banco'
    with app.open_resource('schema.sql', mode='r') as fileToCreateTables:
        db.cursor().executescript(fileToCreateTables.read())
        db.commit()

    

####### ------------------------ ROUTES ----------------------------- #######


									#  -------------------- common ---------------------

@app.route('/')
def redirect_to_devices():
    return redirect(url_for('show_devices_panel'))


@app.route('/error')
def display_error(errorOcurred):
    return render_template('error.html', error = errorOcurred)


def parseDevicesQueryResultToList(devicesFromDb):
    result = list()
    for row in devicesFromDb:
        currentRow = {}
        currentRow["name"] = row[0]
        currentRow["mask"] = row[1]
        currentRow["micro_id"] = row[2]
        currentRow["kind"] = row[3]
        currentRow["localization"] = row[4]
        currentRow["status"] = row[5]
        result.append(currentRow)
    return result
        
       
              

									#  -------------------- devices --------------------

def get_devicesFromDb():
    db = get_db()
    if db is None:
        errorOcurred = {'controller' : 'show_devices_panel', 'details' : 'There is no connection with database'}
        return display_error(errorOcurred)        
    cur = db.execute('select name, mask, micro_id, kind, localization, status from devices order by db_id')
    return cur.fetchall()

@app.route('/stubs/more')
def add_more_stubs():
    db = get_db()
    with app.open_resource('stubs.sql', mode='r') as fileToFillStubs:
        db.cursor().executescript(fileToFillStubs.read())
        db.commit()
    return jsonify(value="true")

@app.route('/stubs/clear')
def clear_stubs():
    db = get_db()
    db.execute("DELETE FROM houseStates WHERE db_id > -1")
    db.commit()
    return jsonify(value="true")

@app.route('/devices/panel')
def show_devices_panel():
    devices_from_db = get_devicesFromDb()
    return render_template('devices_panel.html', showing_devices = devices_from_db)


@app.route('/devices/add', methods=['POST'])
def add_device():
    db = get_db()
    if db is None:
        errorOcurred = {'controller' : 'add_device', 'details' : 'There is no connection with database'}
        return display_error(errorOcurred)

    db.execute('insert into devices (name, mask, micro_id, kind, localization) values (?, ?, ?, ?, ?)', [
      request.form['name'],
      request.form['mask'],
      request.form['micro_id'],
      request.form['kind'],
      request.form['localization']
      ])

    db.commit()
    flash(' Inserido !!')
    return redirect(url_for('show_devices_panel'))


									# 	-------- actions, events and states -----------


@app.route('/status/all')
def get_status_for_devices():
    
    result = parseDevicesQueryResultToList(get_devicesFromDb())
    return jsonify(value=result)   
			
			
@app.route('/status/user')
def get_status_for_user():
    cache = SimpleCache()
    localization = cache.get("user_localization")
    return jsonify(value=localization)


                                    # ------------------- learning ---------------------

@app.route('learning/save-current-states')
def save_current_states():
    bedroomState = houseStateManager.get_current_bedroom_state()
    officeState = houseStateManager.get_current_office_state()
    houseStateManager.save_house_state_in_db(bedroomState)
    houseStateManager.save_house_state_in_db(officeState)
    return jsonify(value="true")

@app.route('learning/trigger-decision')
def trigger_decision():
    decisionService.make_decision(houseStateManager.get_current_office_state())
    decisionService.make_decision(houseStateManager.get_current_bedroom_state())
    return jsonify(value="true")

@app.route('learning/create-trees')
def create_trees():
    decisionService.houseStateRulesManager.create_rules()
    return jsonify(value="true")

@app.route('learning/export-decision-tree/<treeName>')
def export_decision_tree(treeName):
    with open(treeName, 'rb') as f:
        response = make_response(f)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % treeName
        return response


									# 	------------------- house ---------------------


@app.route('/house/panel')
def show_house_panel():
    if(SimpleCache().get("user_localization") is None):
        SimpleCache().set("user_localization", "1")
    return render_template('house_panel.html')
    
    
# cur = db.execute('select status, operator, mic_id, occurred_at from events order by db_id')


# ------------ new controller ---------------
@app.route('/users')
def users_by_room():
    if(SimpleCache().get("users_localizations") is None):
        SimpleCache().set("users_localizations", "1")
    #return render_template('house_panel.html')

@app.route('/office')
def office_devices_control():
    current_office_state = RoomState(0, datetime.datetime.now(), [1,2], True, 19, False)
    # current_office_state = houseStateManager.get_current_office_state()
    users_names = getUsersNameById(current_office_state.users)
    return render_template("office.html",office_state = current_office_state, users_names = users_names)

@app.route('/bedroom')
def bedroom_devices_control():
    return render_template("bedroom_devices.html")

@app.route('/office/light/update/<new_light>')
def office_light_update(new_light):
    house_state_manager.HouseStateManager.change_office_light(int(new_light))
    return jsonify(value=new_light)

@app.route('/bedroom/light/update/<new_light>')
def bedroom_light_update(new_light):
    houseStateManager.change_bedroom_light(int(new_light))
    return jsonify(value=new_light)

@app.route('/office/curtain/update/<new_curtain>')
def office_curtain_update(new_curtain):
    houseStateManager.change_office_curtain(int(new_curtain))
    return jsonify(value= new_curtain)

@app.route('/bedroom/curtain/update/<new_curtain>')
def bedroom_curtain_update(new_curtain):
    houseStateManager.change_bedroom_curtain(int(new_curtain))
    return jsonify(value= new_curtain)


@app.route('/office/temperature/update/<new_temperature>')
def office_temperature_update(new_temperature):
    houseStateManager.change_office_temperature(int(new_temperature))
    return jsonify(value=new_temperature)

@app.route('/bedroom/temperature/update/<new_temperature>')
def bedroom_temperature_update(new_temperature):
    houseStateManager.change_bedroom_temperature(int(new_temperature))
    return jsonify(value=new_temperature)

@app.route('/office/add/<new_user>')
def add_user_to_office(new_user):
    office_state = houseStateManager.get_current_office_state()
    office_state.users.append(int(new_user))
    houseStateManager.save_current_office_state(office_state)
    if len(office_state.users) == 1:
        decisionService.make_decision(office_state)
    return jsonify(value=True)

@app.route('/office/remove/<user>')
def remove_user_from_office(user):
    office_state = houseStateManager.get_current_office_state()
    office_state.users.remove(int(user))
    houseStateManager.save_current_office_state()


def getUsersNameById(usersId):
    users_name = []
    for user_id in usersId:
        if user_id == 0:
            users_name.append('')
        elif user_id == 1:
            users_name.append('Silveira')
        elif user_id == 2:
            users_name.append('Carlos')
        elif user_id == 3:
            users_name.append('Cesar')
        else:
            users_name.append('Convidado')
    return users_name



####### ------------------------ INITIALIZE ----------------------------- #######

if __name__ == "__main__":
    init_db()
    #app.run(host='192.168.0.24', port=2222, debug=True)
    app.run(host='127.0.0.1', port=2222, debug=True) ###Esse e o endereco de localhost

    with app.app_context():
        houseStateManager = house_state_manager()
        decisionService = decision_service()
        devicesControl = devices_control()




