# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://openpg:openpgpwd@localhost:5433/Driver-Behavior'
#
# db = SQLAlchemy(app)
#
#
# class SensorValues(db.Model):
#     __tablename__ = 'sensor_data'
#     id = db.Column(db.Integer, primary_key=True)
#     AccX = db.Column(db.Float)
#     AccY = db.Column(db.Float)
#     AccZ = db.Column(db.Float)
#     GPS_Long = db.Column(db.Float)
#     GPS_Lat = db.Column(db.Float)
#     GyroX = db.Column(db.Float)
#     GyroY = db.Column(db.Float)
#     GyroZ = db.Column(db.Float)
#
#     def __init__(self, AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ):
#         self.AccX = AccX
#         self.AccY = AccY
#         self.AccZ = AccZ
#         self.GPS_Long = GPS_Long
#         self.GPS_Lat = GPS_Lat
#         self.GyroX = GyroX
#         self.GyroY = GyroY
#         self.GyroZ = GyroZ
#
#
# @app.route('/saveData', methods=['POST'])
# def save_data():
#     if request.method == 'POST':
#         AccX = request.form.get('AccX')
#         AccY = request.form.get('AccY')
#         AccZ = request.form.get('AccZ')
#         GPS_Long = request.form.get('GPS_Long')
#         GPS_Lat = request.form.get('GPS_Lat')
#         GyroX = request.form.get('GyroX')
#         GyroY = request.form.get('GyroY')
#         GyroZ = request.form.get('GyroZ')
#
#         data = SensorValues(AccX, AccY, AccZ, GPS_Long, GPS_Lat, GyroX, GyroY, GyroZ)
#         db.session.add(data)
#         db.session.commit()
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
