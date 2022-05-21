from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_sqlalchemy import SQLAlchemy

model = pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://odmysiuiafrwrb:9b9c464723bec07cf7715d0de4fd01fd831441bd75d974a567b8ed72ea7ce476@ec2-34-236-94-53.compute-1.amazonaws.com:5432/d54egu67sh89ou'

db = SQLAlchemy(app)


class SensorValues(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    AccX = db.Column(db.Float)
    AccY = db.Column(db.Float)
    AccZ = db.Column(db.Float)
    GPS_Long = db.Column(db.Float)
    GPS_Lat = db.Column(db.Float)
    GyroX = db.Column(db.Float)
    GyroY = db.Column(db.Float)
    GyroZ = db.Column(db.Float)

    def __init__(self, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ):
        self.AccX = AccX
        self.AccY = AccY
        self.AccZ = AccZ
        self.GPS_Long = GPS_Long
        self.GPS_Lat = GPS_Lat
        self.GyroX = GyroX
        self.GyroY = GyroY
        self.GyroZ = GyroZ


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

        data = SensorValues(AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ)
        db.session.add(data)
        db.session.commit()


@app.route('/')
def home():
    return "Hello World"


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


@app.route('/lol')
def home_1():
    return "Hello World"


if __name__ == '__main__':
    app.run(debug=True)
