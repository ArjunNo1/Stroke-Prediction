
from flask import Flask,  request, render_template
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


app = Flask(__name__)
stroker = pickle.load(open("model.pkl", "rb"))


@app.route('/analysis')
def analysis():
    return render_template("stroke.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        gender = request.form["gender"]
        age = request.form["age"]
        hypertension = request.form["hypertension"]
        disease = request.form["disease"]
        married = request.form["married"]
        work = request.form["work"]
        residence = request.form["residence"]
        glucose = request.form["glucose"]
        bmi = request.form["bmi"]
        smoking = request.form["smoke"]

        # gender
        if (gender == "Male"):
            gender_Male = 1
            gender_Other = 0
        elif(gender == "Others"):
            gender_Male = 1
            gender_Other = 0
        else:
            gender_Male = 0
            gender_Other = 0

        if (married == "yes"):
             ever_married_Yes = 1
        else:
             ever_married_Yes = 0

        if(work == 'Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_children = 0
            work_type_Self_employed = 1
        elif(work == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_children = 0
            work_type_Self_employed = 0
        elif(work == 'Children'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_children = 1
            work_type_Self_employed = 0
        elif(work == 'Not Worked'):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_children = 0
            work_type_Self_employed = 0
        else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_children = 0
            work_type_Self_employed = 0
        if(residence == 'Urban'):
            Residence_type_Urban = 1
        else:
            Residence_type_Urban = 0

        if(smoking == 'Never Smoked'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
        elif(smoking == 'Formerly Smoke'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
        elif(smoking == 'Smoke Frequently'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
        else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0

        feature = scaler.fit_transform([[age, hypertension, disease, glucose,
       bmi, gender_Male, gender_Other, ever_married_Yes,
       work_type_Never_worked, work_type_Private,
       work_type_Self_employed, work_type_children, Residence_type_Urban,
       smoking_status_formerly_smoked, smoking_status_never_smoked,
       smoking_status_smokes]])

        prediction=stroker.predict(feature)
        print(prediction)

        return render_template("index.html",prediction_text="Chance of stroke prediction is  {}".format(prediction))


    else:

        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
