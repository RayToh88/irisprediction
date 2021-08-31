from flask import Flask,jsonify,request,g,render_template
from flask.templating import render_template
from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:
    @classmethod

    def getUsers(cls): 
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary =True)  # dictionary is to convert json fromat

        sql = "select * from user"
        cursor.execute(sql)
        users= cursor.fetchall()               #[please take note two thing the spelling and def]
        return users



    @classmethod
    def UserByUserid(cls,userid): 
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary =True)  # dictionary is to convert json fromat

            sql = "select * from user where userid=%s"
            cursor.execute(sql,(userid,))           # Here take note the () is the searching of userid
            users= cursor.fetchall()               #[please take note two thing the spelling and def]
            return users
        finally:
            dbConn.close()

    @classmethod
    def insertUser(cls,username,email,passsword):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="insert into user(username,email,passsword) values(%s,%s,%s)"
            cursor.execute(sql,(username,email,passsword))
            dbConn.commit()

            count=cursor.rowcount

            print(cursor.lastrowid)
            

            return count
        finally:
            dbConn.close()



    @classmethod
    def insertUser2(cls,sepalLength,sepalWidth,petalLength,petalWidth):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="insert into irispredictiontable(sepalLength,sepalWidth,petalLength,petalWidth) values(%s,%s,%s,%s)"
            cursor.execute(sql,(sepalLength,sepalWidth,petalLength,petalWidth))
            dbConn.commit()

            count=cursor.rowcount
            p = cursor.lastrowid
            print(p)

            return count
        finally:
            dbConn.close()

    @classmethod
    def updateUser(cls,userid,email,passsword):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="update user set email=%s,passsword=%s where userid=%s"
            cursor.execute(sql,(email,passsword,userid))
            dbConn.commit()
            count=cursor.rowcount

            return count
        finally:
            dbConn.close()

    @classmethod
    def deleteUser(cls,id):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="delete from irispredictiontable where id=%s"
            cursor.execute(sql,(id,))
            dbConn.commit()
            count=cursor.rowcount

            return count
        finally:
            dbConn.close()
    @classmethod
    def loginUser(cls,userJSON):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql="select * from user where username=%s and passsword=%s"
            cursor.execute(sql,(userJSON["username"],userJSON["passsword"]))
            user=cursor.fetchone()

            #---jwt encode to generate a token----
            
            if user==None:
                return {"jwt":""}             # Return null vaule
            #else:
                #return users          # Fetch invidual record
            
            else:
                passsword=user['passsword']
                userid=user['userid']
                username=user['username']
                ray = "Hi how are u"
                # Below will be the message u wish to put in the payload, and the expired time
                jwtToken=jwt.encode({"passsword":passsword,"username":username,"exp":datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)},Settings.secretKey,"HS256")

                print(jwtToken)
                return {"jwt":jwtToken}
            
        finally:
            dbConn.close()