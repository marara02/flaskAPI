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

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://warsvbczvqigvl:bc7e4b24cebdb29ac8213a91733166bad6acbec63c8c4ccfd94034579265343a@ec2-52-44-13-158.compute-1.amazonaws.com:5432/d4j0960vbacuc'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
sched = BlockingScheduler()


class JsonModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Users table
class UserFinal(db.Model, JsonModel):
    __tablename__ = 'user_final'
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


# Initial sensor database
class SensorValues(db.Model, JsonModel):
    __tablename__ = 'sensor_data_upd'
    id = db.Column(db.Integer, primary_key=True)
    driving_name = db.Column(db.String(255))
    AccX = db.Column(db.Float)
    AccY = db.Column(db.Float)
    AccZ = db.Column(db.Float)
    GPS_Long = db.Column(db.Float)
    GPS_Lat = db.Column(db.Float)
    GyroX = db.Column(db.Float)
    GyroY = db.Column(db.Float)
    GyroZ = db.Column(db.Float)
    timestamp = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user_final.id'))

    # request = db.relationship("User", backref=backref("user_final", uselist=False))

    def __init__(self, driving_name, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ, timestamp, user_id):
        self.driving_name = driving_name
        self.AccX = AccX
        self.AccY = AccY
        self.AccZ = AccZ
        self.GPS_Long = GPS_Long
        self.GPS_Lat = GPS_Lat
        self.GyroX = GyroX
        self.GyroY = GyroY
        self.GyroZ = GyroZ
        self.timestamp = timestamp
        self.user_id = user_id


# Final results database with ratings
class DriverRates(db.Model, JsonModel):
    __tablename__ = 'driver_rate_total_upd'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_final.id'))
    driving_name = db.Column(db.String(255))
    timestamp_start = db.Column(db.String(100))
    timestamp_end = db.Column(db.String(100))
    gps_lat_1 = db.Column(db.Float)
    gps_long_1 = db.Column(db.Float)
    gps_lat_2 = db.Column(db.Float)
    gps_long_2 = db.Column(db.Float)
    acceleration_rate = db.Column(db.Integer)
    braking_rate = db.Column(db.Integer)
    cornering_rate = db.Column(db.Integer)
    safety_score = db.Column(db.Integer)

    # request = db.relationship("User", backref=backref("user_final", uselist=False))

    def __init__(self, user_id, driving_name, timestamp_start, timestamp_end, gps_lat_1, gps_long_1, gps_lat_2,
                 gps_long_2, acceleration_rate, braking_rate,
                 cornering_rate,
                 safety_score):
        self.user_id = user_id
        self.driving_name = driving_name
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.gps_lat_1 = gps_lat_1
        self.gps_lat_2 = gps_lat_2
        self.gps_long_1 = gps_long_1
        self.gps_long_2 = gps_long_2
        self.acceleration_rate = acceleration_rate
        self.braking_rate = braking_rate
        self.cornering_rate = cornering_rate
        self.safety_score = safety_score


# Second table with sensors and results
class SensorValuesWithTarget(db.Model, JsonModel):
    __tablename__ = 'sensor_data_target'
    id = db.Column(db.Integer, primary_key=True)
    driving_name = db.Column(db.String(255))
    GPS_Long = db.Column(db.Float)
    GPS_Lat = db.Column(db.Float)
    Target = db.Column(db.Integer)

    def __init__(self, driving_name, GPS_Long, GPS_Lat, Target):
        self.driving_name = driving_name
        self.GPS_Long = GPS_Long
        self.GPS_Lat = GPS_Lat
        self.Target = Target
