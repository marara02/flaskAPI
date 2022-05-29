import json

from flask import Flask, request, jsonify, Blueprint, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import pandas as pd
# import pandas as pd
from flask_sqlalchemy import SQLAlchemy

model = pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://odmysiuiafrwrb:9b9c464723bec07cf7715d0de4fd01fd831441bd75d974a567b8ed72ea7ce476@ec2-34-236-94-53.compute-1.amazonaws.com:5432/d54egu67sh89ou'

db = SQLAlchemy(app)


class JsonModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SensorValues(db.Model, JsonModel):
    __tablename__ = 'sensor_data_upd'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100))
    AccX = db.Column(db.Float)
    AccY = db.Column(db.Float)
    AccZ = db.Column(db.Float)
    GPS_Long = db.Column(db.Float)
    GPS_Lat = db.Column(db.Float)
    GyroX = db.Column(db.Float)
    GyroY = db.Column(db.Float)
    GyroZ = db.Column(db.Float)

    def __init__(self, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ, timestamp):
        self.timestamp = timestamp
        self.AccX = AccX
        self.AccY = AccY
        self.AccZ = AccZ
        self.GPS_Long = GPS_Long
        self.GPS_Lat = GPS_Lat
        self.GyroX = GyroX
        self.GyroY = GyroY
        self.GyroZ = GyroZ


class DriverRates(db.Model, JsonModel):
    __tablename__ = 'driver_rate_total'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer)
    timestamp_start = db.Column(db.String(100))
    timestamp_end = db.Column(db.String(100))
    acceleration_rate = db.Column(db.Integer)
    braking_rate = db.Column(db.Integer)
    cornering_rate = db.Column(db.Integer)
    safety_score = db.Column(db.Integer)

    def __init__(self, driving_id, timestamp_start, timestamp_end, acceleration_rate, braking_rate, cornering_rate,
                 safety_score):
        self.driving_id = driving_id
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.acceleration_rate = acceleration_rate
        self.braking_rate = braking_rate
        self.cornering_rate = cornering_rate
        self.safety_score = safety_score


class SensorValuesWithTarget(db.Model, JsonModel):
    __tablename__ = 'sensor_data_target'
    id = db.Column(db.Integer, primary_key=True)
    AccX = db.Column(db.Float)
    AccY = db.Column(db.Float)
    AccZ = db.Column(db.Float)
    GPS_Long = db.Column(db.Float)
    GPS_Lat = db.Column(db.Float)
    GyroX = db.Column(db.Float)
    GyroY = db.Column(db.Float)
    GyroZ = db.Column(db.Float)
    Target = db.Column(db.Integer)

    def __init__(self, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ, Target):
        self.AccX = AccX
        self.AccY = AccY
        self.AccZ = AccZ
        self.GPS_Long = GPS_Long
        self.GPS_Lat = GPS_Lat
        self.GyroX = GyroX
        self.GyroY = GyroY
        self.GyroZ = GyroZ
        self.Target = Target


class Users(db.Model, JsonModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, email, password, username, name, phone):
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    phone = request.form.get('phone')

    user = Users.query.filter_by(username=username).first()
    if user is None:
        new_user = Users(email=email, username=username, password=password, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(["Register success"])
    else:
        return jsonify(["Username exist already exist"])


@app.route("/login", methods=["GET", "POST"])
def login_post():
    d = {}
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login = Users.query.filter_by(username=username, password=password).first()
        if login is None:
            return jsonify(["Wrong Credentials"])
        else:
            return jsonify(["success"])


@app.route('/')
def home():
    return "Hello World"


@app.route('/saveData', methods=['POST'])
def save_data():
    if request.method == 'POST':
        AccX = request.form.get('AccX')
        AccY = request.form.get('AccY')
        AccZ = request.form.get('AccZ')
        GPS_Long = request.form.get('GPS_Long')
        GPS_Lat = request.form.get('GPS_Lat')
        GyroX = request.form.get('GyroX')
        GyroY = request.form.get('GyroY')
        GyroZ = request.form.get('GyroZ')
        timestamp = request.form.get('TimeStamp')

        data = SensorValues(AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ, timestamp)
        db.session.add(data)
        db.session.commit()
        return "Written!"


@app.route('/deleteSensors', methods=['DELETE'])
def delete_data():
    db.session.query(SensorValues).delete()
    db.session.commit()
    return "Deleted"


@app.route('/deleteResults', methods=['DELETE'])
def delete_results():
    db.session.query(DriverRates).delete()
    db.session.commit()
    return "Deleted"


@app.route('/getAllSensorData', methods=['GET'])
def get_data():
    return json.dumps([ss.as_dict() for ss in SensorValues.query.all()])


@app.route('/getUsers', methods=['GET'])
def get_user():
    return json.dumps([ss.as_dict() for ss in Users.query.all()])


@app.route('/getResult', methods=['GET'])
def get_result():
    js = pd.read_json(json.dumps([ss.as_dict() for ss in SensorValues.query.all()]))
    tst = js['timestamp'][0]
    tet = js['timestamp'].iloc[-1]
    del js['id']
    del js['timestamp']
    result = model.predict(js)
    new_result = []
    for i in result:
        new_result.append(i)
    acceleration_times = [x for x in new_result if x == 0]
    braking_times = [x for x in new_result if x == 1]
    cornering_times = [x for x in new_result if x == 2]
    acceleration_rate = len(acceleration_times)
    braking_rate = len(braking_times)
    cornering_rate = len(cornering_times)
    safety_score = 100 - acceleration_rate - braking_rate - cornering_rate
    dct = {
        "time_start": tst,
        "time_end": tet,
        "acceleration_rate": acceleration_rate,
        "braking_rate": braking_rate,
        "cornering_rate": cornering_rate,
        "safety_score": safety_score
    }
    return dct


@app.route('/sendEndResult', methods=['POST'])
def send_end_result_of_driver():
    dct = get_result()
    start = dct['time_start']
    end = dct['time_end']
    acr = dct['acceleration_rate']
    br = dct['braking_rate']
    corn = dct['cornering_rate']
    scr = dct["safety_score"]
    data = DriverRates(1, start, end, acr, br, corn, scr)
    db.session.add(data)
    db.session.commit()
    return "Written to result database"


@app.route('/historyResult', methods=['GET'])
def get_history_driver_rate():
    return json.dumps({"Driver": [ss.as_dict() for ss in DriverRates.query.all()]})


@app.route('/predict', methods=['POST'])
def predict():
    AccX = request.form.get('AccX')
    AccY = request.form.get('AccY')
    AccZ = request.form.get('AccZ')
    GyroX = request.form.get('GyroX')
    GyroY = request.form.get('GyroY')
    GyroZ = request.form.get('GyroZ')
    input_query = np.array([[GyroX, GyroY, GyroZ, AccX, AccY, AccZ]])
    result = model.predict(input_query)[0]
    return jsonify({'Y': str(result)})


if __name__ == '__main__':
    app.run(debug=True)
