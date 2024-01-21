import pickle
import numpy as np
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load the trained model from the pickle file
with open('E:/Hacktopia-GNI/code/sleep_analysis/modelll.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['Age'])
    gender = int(request.form['Gender'])
    sleep_duration = float(request.form['sleep_duration'])
    rem_percentage = int(request.form['rem_percentage'])
    deep_percentage = int(request.form['deep_percentage'])
    light_percentage = int(request.form['light_percentage'])
    awakenings = float(request.form['awakenings'])
    caffeine = float(request.form['caffeine'])
    alcohol = float(request.form['alcohol'])
    smoking = int(request.form['smoking'])
    exercise = float(request.form['exercise'])

    features = np.array([[age, gender, sleep_duration, rem_percentage, deep_percentage, light_percentage,
                          awakenings, caffeine, alcohol, smoking, exercise]])

    sleep_efficiency_prediction = model.predict(features)[0]
    sleep_efficiency_prediction=round(sleep_efficiency_prediction, 2)
    if sleep_efficiency_prediction > 0.70:
        return redirect(url_for('positive', prediction=sleep_efficiency_prediction))
    else:
        return redirect(url_for('negative', prediction=sleep_efficiency_prediction))

@app.route('/positive')
def positive():
    prediction = float(request.args.get('prediction'))
    return render_template('positive.html', prediction=prediction)

@app.route('/negative')
def negative():
    prediction = float(request.args.get('prediction'))
    return render_template('negative.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)