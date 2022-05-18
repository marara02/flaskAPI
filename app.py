from flask import Flask, request, jsonify
import pickle
import numpy as np

model = pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
