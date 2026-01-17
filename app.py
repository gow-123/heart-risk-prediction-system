
from flask import Flask, render_template, request, redirect
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open("heart_model.pkl", "rb"))

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/patient')
def patient():
    return render_template('patient_form.html')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return redirect('/')
    try:
        male=float(request.form.get('male',0))
        age=float(request.form.get('age',0))
        education=float(request.form.get('education',0))
        currentSmoker=float(request.form.get('currentSmoker',0))
        cigsPerday=float(request.form.get('cigsPerDay',0))
        BPMeds=float(request.form.get('BPMeds',0))
        prevalentStroke=float(request.form.get('prevalentStroke',0))
        prevalentHype=float(request.form.get('prevalentHype',0))
        diabetes=float(request.form.get('diabetes',0))
        totChol=float(request.form.get('totChol',0))
        sysBP=float(request.form.get('sysBP',0))
        diaBP=float(request.form.get('diaBP',0))
        BMI=float(request.form.get('BMI',0))
        heartrate=float(request.form.get('heartRate',0))
        glucose=float(request.form.get('glucose',0))
        
        if not (10<=BMI<=60):
            raise ValueError("BMI out of range")
        
        if not (30<=heartrate<=200):
            raise ValueError('Heart rate out of range')
        
        if not (50<=glucose<=300):
            raise ValueError('Glucose out of range')
        
            


        final_features = np.array([[male,age,education,currentSmoker,cigsPerday,BPMeds,prevalentStroke,prevalentHype,diabetes,totChol,sysBP,diaBP,BMI,heartrate,glucose]])
        prediction = model.predict(final_features)[0]
        try:
            probability = model.predict_proba(final_features)[0][1] * 100
        except:
            probability = None

        if prediction == 1:
            result = "Heart Disease Detected ❤️"
            risk = f"High Risk ({probability:.2f}%)" if probability else "High Risk"
        else:
            result = "No Heart Disease 💚"
            risk = f"Low Risk ({probability:.2f}%)" if probability else "Low Risk"

    

        return render_template('result.html', prediction=int(prediction),probability=round(probability, 2),risk=risk)
    except ValueError:
        return render_template('result.html',prediction="Invalid input ❌",risk="Please enter valid medical values")

    except Exception:
        return render_template(
            'result.html',
            prediction="Something went wrong ⚠️",
            risk="Try again later"
        )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
