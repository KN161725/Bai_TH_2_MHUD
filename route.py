from flask import render_template,redirect,request,url_for,session
from urllib.parse import urlparse
import joblib
import numpy as np
import string
import secrets

def get_label(i):
    label_mapping = ['Setosa', 'Versicolor', 'Virginica']
    return label_mapping[i]
def set_route(app):
    model=joblib.load('knn_model.joblib')
    @app.route("/")
    def Home_page():
        return render_template("Home_page2.html")
    
    @app.route("/input_data",methods=["GET","POST"])
    def input_data():
        if request.method=="POST":
            rq=request
            if rq!=None:    
                count=0
                try:
                    sepal_length=float(rq.form["sepal_length"])
                except:
                    sepal_length="Invalid"
                    count+=1
                
                try:
                    sepal_width=float(rq.form["sepal_width"])
                except:
                    sepal_width="Invalid"
                    count+=1
                
                try:
                    petal_length=float(rq.form["petal_length"])
                except:
                    petal_length="Invalid"
                    count+=1
                
                try:
                    petal_width=float(rq.form["petal_width"])
                except:
                    petal_width="Invalid"
                    count+=1
    
                if count>0:
                    dict_=dict(sepal_length=sepal_length,sepal_width=sepal_width,petal_length=petal_length,petal_width=petal_width)
                    return render_template("Error_Input.html",**dict_)
                y_pred=model.predict([[sepal_length,sepal_width,petal_length,petal_width]])
                session['Result']=get_label(np.argmax(y_pred,axis=1)[0])
                return redirect(url_for('result'))
            return render_template("Input_data2.html")
        return render_template("Input_data2.html")
    
    @app.route("/result")
    def result():
        #Secure 
        rff=request.headers.get("Referer")
        url_cur=urlparse(rff)
        
        if (rff!=None) & (url_cur.path==url_for('input_data')):
            return render_template("Result.html",y_pred=session['Result'])
        else: return redirect(url_for('Home_page'))
        

def secret_key(tmp):
    chars=string.digits+string.ascii_letters+string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(tmp))
    
