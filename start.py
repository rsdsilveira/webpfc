####### ------------------------ IMPORTS ----------------------------- #######

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.contrib.cache import SimpleCache

import house_state_manager
#from HouseStateManager import HouseStateManager
#from house_state_manager import HouseStateManager
import decision_service
import devices_control

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
    with app.open_resource('stubs.sql', mode='r') as fileToFillStubs:
        db.cursor().executescript(fileToFillStubs.read())
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
    
@app.route('/actions/do')
def do_action_for_device():
#			micro_id = request.args.get('micro_id',0, type=int)
#			ocurred_date = date.now()
#			# finge que interagiu
#			# salva evento no banco - quem fez foi a casa entao operator = 1
			# muda status no cache
			return jsonify(result='A')
			
			
@app.route('/status/all')
def get_status_for_devices():
    
    result = parseDevicesQueryResultToList(get_devicesFromDb())
    return jsonify(value=result)   
			
			
@app.route('/status/user')
def get_status_for_user():
    cache = SimpleCache()
    localization = cache.get("user_localization") 			
    return jsonify(value=localization)   
						
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
    return render_template("office.html")

@app.route('/bedroom')
def bedroom_devices_control():
    return render_template("bedroom_devices.html")

@app.route('/office/light/update/<new_light>')
def office_light_update(new_light):
    house_state_manager.HouseStateManager.change_office_light(new_light)
    return jsonify(value=new_light)

@app.route('/bedroom/light/update/<new_light>')
def bedroom_light_update(new_light):
    houseStateManager.change_bedroom_light(new_light)
    return jsonify(value=new_light)

@app.route('/office/curtain/update/<new_curtain>')
def office_curtain_update(new_curtain):
    houseStateManager.change_office_curtain(new_curtain)
    return jsonify(value= new_curtain)

@app.route('/bedroom/curtain/update/<new_curtain>')
def bedroom_curtain_update(new_curtain):
    houseStateManager.change_bedroom_curtain(new_curtain)
    return jsonify(value= new_curtain)


@app.route('/office/temperature/update/<new_temperature>')
def office_temperature_update(new_temperature):
    houseStateManager.change_office_temperature(new_temperature)
    return jsonify(value=new_temperature)

@app.route('/bedroom/temperature/update/<new_temperature>')
def bedroom_temperature_update(new_temperature):
    houseStateManager.change_bedroom_temperature(new_temperature)
    return jsonify(value=new_temperature)

@app.route('/office/<user>')
def add_user_to_office(new_user):
    office_state = houseStateManager.get_current_office_state()
    office_state.users.append(new_user)
    houseStateManager.save_current_office_state(office_state)
    if len(office_state.users) == 1:
        decisionService.make_decision(office_state)
    return jsonify(value=True)


def remove_user_from_office(user):
    office_state = houseStateManager.get_current_office_state()
    office_state.users.remove(user)
    houseStateManager.save_current_office_state()




####### ------------------------ INITIALIZE ----------------------------- #######

if __name__ == "__main__":
    init_db()
    #app.run(host='200.20.121.234', port=2222, debug=True)
    app.run(host='127.0.0.1', port=2222, debug=True)

    with app.app_context():
        houseStateManager = house_state_manager()
        decisionService = decision_service()
        devicesControl = devices_control()




