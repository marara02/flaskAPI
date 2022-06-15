import json

from flask import Flask, request, jsonify, Blueprint, url_for, redirect
from flask_migrate import Migrate
from sqlalchemy import inspect
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import pandas as pd
# import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.blocking import BlockingScheduler
from model import base as bs

model = pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://warsvbczvqigvl:bc7e4b24cebdb29ac8213a91733166bad6acbec63c8c4ccfd94034579265343a@ec2-52-44-13-158.compute-1.amazonaws.com:5432/d4j0960vbacuc'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
sched = BlockingScheduler()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# Sign up endpoint
@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    phone = request.form.get('phone')

    user = bs.UserFinal.query.filter_by(username=username).first()
    if user is None:
        new_user = bs.UserFinal(email=email, username=username, password=password, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(["Register success"])
    else:
        return jsonify(["Username exist already exist"])


# Sign in endpoint
@app.route("/login", methods=["GET", "POST"])
def login_post():
    d = {}
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login = bs.UserFinal.query.filter_by(username=username, password=password).first()
        # user_id = UserFinal.query.with_entities(UserFinal.id).filter_by(username=username, password=password).first()
        if login is None:
            return jsonify(["Wrong Credentials"])
        else:
            d = object_as_dict(login)
            print(d)
            json.dumps({"User": [d]})
            return json.dumps({"User": [d]})


# Endpoint for writing to database about sensor values
@app.route('/saveData', methods=['POST'])
def save_data():
    if request.method == 'POST':
        driving_name = request.form.get('driving_name')
        AccX = request.form.get('AccX')
        AccY = request.form.get('AccY')
        AccZ = request.form.get('AccZ')
        GPS_Long = request.form.get('GPS_Long')
        GPS_Lat = request.form.get('GPS_Lat')
        GyroX = request.form.get('GyroX')
        GyroY = request.form.get('GyroY')
        GyroZ = request.form.get('GyroZ')
        timestamp = request.form.get('TimeStamp')
        user_id = request.form.get('user_id')

        data = bs.SensorValues(driving_name, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ, timestamp,
                            user_id)
        db.session.add(data)
        db.session.commit()
        return "Written!"


# Deleting data from initial sensor database
@sched.scheduled_job('cron', day_of_week='mon-fri', hour='0-9', minute='30-59', second='*/3')
@app.route('/deleteSensors', methods=['DELETE'])
def delete_data():
    db.session.query(bs.SensorValues).delete()
    db.session.commit()
    return "Deleted"


# Deleting data from rating table
@app.route('/deleteResults', methods=['DELETE'])
def delete_results():
    db.session.query(bs.DriverRates).delete()
    db.session.commit()
    return "Deleted"


# Get all sensor values for check
@app.route('/getAllSensorData', methods=['GET'])
def get_data():
    return json.dumps([ss.as_dict() for ss in bs.SensorValues.query.all()])


# Getting all users from database
@app.route('/getUsers', methods=['GET'])
def get_user():
    return json.dumps([ss.as_dict() for ss in bs.UserFinal.query.all()])


# Get data from sensor table and implement Ml, then send results to History table
@app.route('/GetDriverLastData/<int:user_id>/<string:driving_name>', methods=['POST', 'GET'])
def read_last_driving_of_driver(user_id: int, driving_name: str):
    js = pd.read_json(json.dumps([ss.as_dict() for ss in
                                  bs.SensorValues.query.filter_by(user_id=user_id, driving_name=driving_name)]))
    tst = js['timestamp'][0]
    tet = js['timestamp'].iloc[-1]
    del js['id']
    del js['timestamp']
    del js['user_id']
    del js['driving_name']
    result = model.predict(js)
    new_result = []
    new_result_1 = []
    new_result_2 = []
    for i in result:
        new_result.append(i)
    for j in js['GPS_Long']:
        new_result_1.append(j)
    for k in js['GPS_Lat']:
        new_result_2.append(k)
    acceleration_times = [x for x in new_result if x == 0]
    braking_times = [x for x in new_result if x == 1]
    cornering_times = [x for x in new_result if x == 2]
    acceleration_rate = len(acceleration_times)
    braking_rate = len(braking_times)
    cornering_rate = len(cornering_times)
    safety_score = 100 - acceleration_rate - braking_rate - cornering_rate
    data = bs.DriverRates(user_id, driving_name, tst, tet, new_result_2[0], new_result_1[0], new_result_2[-1],
                       new_result_1[-1], acceleration_rate, braking_rate, cornering_rate, safety_score)
    db.session.add(data)
    db.session.commit()
    return "Written to result database"


# Get driver history by user username
@app.route('/historyResult', methods=['GET'])
def get_history_driver_rate(username):
    return json.dumps({"Driver": [ss.as_dict() for ss in bs.DriverRates.query.filter_by(username=username)]})


@app.route('/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id: int):
    return json.dumps({"User_result": [ss.as_dict() for ss in bs.DriverRates.query.filter_by(user_id=user_id)]})


if __name__ == '__main__':
    app.run(debug=True)
