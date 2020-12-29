from flask import Flask,request, jsonify, render_template
import pickle
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
#import os
#from pathlib import Path
app = Flask(__name__)
#dire='C:\\Users\\USER\\Desktop\\NEW DEPLOYMENT\\model.pkl'

model=pickle.load(open("model.pkl","rb"))
scalerr=pickle.load(open("scale.pkl","rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
  
    
    num=[request.form["age"],request.form["systolic"],request.form["diastolic"],request.form["pulse"],request.form["bmi"]]
    numeric=[[float(i) for i in num]]
    
    cat=[[request.form["gender"],request.form["cholesterol"],request.form["glucose"],request.form["smoke"],
          request.form["alcohol"],request.form["active"]]]
    ohe=OneHotEncoder()
    test=cat[0]
    def func(alist):
        if alist[0]=="male":
            a=[1,0]
        else:
            a=[0,1]
        if alist[1]=="above normal":
            b=[1,0,0]
        elif alist[1]=="extreme":
            b=[0,1,0]
        else:
            b=[0,0,1]
        if alist[2]=="above normal":
            c=[1,0,0]
        elif alist[2]=="extreme":
            c=[0,1,0]
        else:
            c=[0,0,1]
        if alist[3]=="no":
            d=[1,0]
        else:
            d=[0,1]
        if alist[4]=="no":
            e=[1,0]
        else:
            e=[0,1]
        if alist[5]=="no":
            f=[1,0]
        else:
            f=[0,1]
        return a+b+c+d+e+f
    
    main_cat=func(test)
    category=[main_cat]
    new_num=scalerr.transform(numeric)
    overall=np.hstack([new_num,category])
    pred=model.predict(overall)
    return render_template("index.html",prediction_text=pred)
    




if __name__ == '__main__':
    
    app.run()