from flask import Flask,jsonify,request,g,render_template,abort,make_response,redirect
import re
import bcrypt
from flask_cors import CORS
from model.user import User         # Here is import the model from your own file app and defition
from Validation.Validator import *  # Here import every single thing
import numpy as np
import pickle
16

model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)
CORS(app)     # Here to somehow or other here is to link your using html code without this it will have error

@app.route('/')
@login_required
def home():
      return render_template('index.html')

@app.route('/predict',methods=['POST'])
@login_required
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
   
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output =prediction[0]
    userData=request.json
    sepalLength=request.form['SepalLength']
    sepalWidth=request.form['SepalWidth']
    petalLength=request.form['PetalLength']
    petalWidth=request.form['PetalWidth']
    p = (sepalLength,sepalWidth,petalLength,petalWidth)
    #call model to insert 
    insert = User.insertUser2(sepalLength,sepalWidth,petalLength,petalWidth)
    objarr = [{"index":sepalLength ,"number":"SepalLength is ","index":sepalLength},{"index":sepalWidth,"number":"SepalWidth is"},{"index":petalLength,"number":"PetalLength is"},
    {"index":petalWidth,"number":"PetalWidth is"},]
    return render_template('index.html', prediction_text='The Flower is {}'.format(output),
    sl=sepalLength,sw=sepalWidth,pl=petalLength,pw=petalWidth,rows=objarr,arr=[2,4,6,8])

@app.route("/signup",methods=['POST']) #is reslove after i use str html
def signup():
    print("formsubmit route")
    try:
        #extract the incoming request data from user
        userData=request.json  #request.form.to_dict() ->if using html forms
        print(userData)
        #userid=userData['userid']
        username=request.form['username']
        email=request.form['email']
        passsword=request.form['pws']
        #call model to insert 
        insert = User.insertUser(username,email,passsword)
        return render_template('signup.html')
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500

@app.route('/<string:url>') # This is for html code 
def staticPage(url):
    print("static page",url)
    try:
        return render_template(url)
    except Exception as err:
        abort(404)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        
        count=User.deleteUser(id)
        print(count)
        return redirect("/")
    
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500


@app.route('/login',methods=['POST'])   # We have insert the data in 
def login():
    try:
        username=request.form['username']
        pwd=request.form['pwd']
        output=User.loginUser({"username":username,"passsword":pwd})
        print(output)
        print(jwt)
        if output["jwt"]=="":
            return render_template("login.html",message="Invalid Login Credentials!")
       
        else:
            resp = make_response(render_template("index.html"))
            resp.set_cookie('jwt', output["jwt"])
    
            return resp
    except Exception as err:
        print(err)
        return render_template("login.html",message="Error!")

@app.route('/logout') #define the api route
def logout():
    resp = make_response(redirect("login.html"))
    resp.delete_cookie('jwt')
    
    return resp


if __name__ == '__main__':
    app.run(debug=True)