import os

class Settings:
    secretKey="521897kdbmgj321djnbug#@4rhxcjk6(!d)" # this is bascially for the jwt to encode it 

        #Staging on heroku
    host=os.environ['HOST']
    database=os.environ['DataBase']
    user=os.environ['USERNAME']
    password=os.environ['Password']