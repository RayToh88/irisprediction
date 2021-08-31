from flask import Flask,jsonify,render_template,request,g,redirect
from config.Settings import Settings
import functools
import jwt
from model.user import User  

def login_required(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        auth=True
        auth_token=request.cookies.get("jwt")
        print(auth_token)

        if auth_token==None:
            auth=False
        
        '''
        auth_header = request.headers.get('Authorization') #retrieve authorization bearer token
        if auth_header: 
            auth_token = auth_header.split(" ")[1]#retrieve the JWT value without the Bearer 
        else:
            auth_token = ''
            auth=False #Failed check
        '''    
        if auth_token:
            try:
                payload = jwt.decode(auth_token,Settings.secretKey,algorithms=['HS256'])
                #print(payload)
                g.password=payload['passsword']#update info in flask application context's g which lasts for one req/res cyycle
                g.username=payload['username']

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth=False #Failed check

        if auth==False:

            #return jsonify({"Message":"Not Authorized!"}),403 #return response
            return redirect("login.html")
        return func(*args, **kwargs)

    return secure_login




def admin_required(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        if g.role == ("admin"):

           auth = True

        else:
            auth = False
            output={"Message":"You are not admin"}
            print(g.role)    # Checking g.role funtion
            return jsonify(output),403

        value = func(*args, **kwargs)
            # Do something after
        return value
    return wrapper_decorator

def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        if g.role == ("admin"):   
            auth = True

        # I am forcing them to excute to see it own userid only that all other infomration unable to see    
        elif g.role == ("user"):
            users = User.UserByUserid(g.iduser)
            output={"Users":users}
            return jsonify(output),200
        else:
            #Basically think this is no use soo all define is user ( Here memmber unable to log in)
            output={"Message":"You are not user and admin"}
            print(g.role)    # Checking g.role funtion
            return jsonify(output),403

        value = func(*args, **kwargs)
            # Do something after
            
        return value
    return wrapper_decorator