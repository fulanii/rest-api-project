

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)


# my local imports
from flask_package import  routes # diff way to inport: from . routes import * 

