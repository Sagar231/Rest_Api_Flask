from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.users import UserRegister
from resources.items import Item,ItemList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key = "Sagar_key"
api = Api(app)

jwt = JWT(app,authenticate,identity) #/auth

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == "__main__":
   db.init_app(app)
   app.run(port = 5000,debug = True)
