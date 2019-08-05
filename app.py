import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Itemlist, Item
from resources.store import StoreList, Stores



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  os.environ.get("DATABASE_URL","sqlite:///db/data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("URI_ONE","1234tek")
api = Api(app)

jwt = JWT(app, authenticate, identity)  # generates /auth endpoint

api.add_resource(Stores,"/store/<string:name>")
api.add_resource(StoreList,"/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Itemlist, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
