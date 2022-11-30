

from flask import render_template, jsonify, request
from flask_restful import Resource, Api, reqparse

# my local imports
from flask_package import app, api
from .postgres_package import MyDb 

db = MyDb()

@app.route("/")
def home():
    return render_template("home.html")


# API # API 
# API # API 

## GET endpoints # GET endpoints
class get_all_countries(Resource):
    """:GET Returns all the countries and their info from the database """
    def get(self):
        data = db.return_data_dict()
        return data
api.add_resource(get_all_countries, '/allcountries')

class get_amount_countries(Resource):
    """:GET Returns a predetermined amount of countries and their info from the database, use :num_countries param to set amount"""
    def get(self, num_countries:int):
        print(num_countries)
        data = db.return_data_dict(num_rows=num_countries)
        return data
api.add_resource(get_amount_countries, '/getcountries/<int:num_countries>')

class get_country_name(Resource):
    """ :GET a country and it's info using its's name, use :name to set the country name """
    def get(self, name:str):
        data = db.get_by_name(name)
        return data
api.add_resource(get_country_name, '/getcountry/<string:name>')


## POST endpoints # POST endpoints
class add_country_code(Resource):
    """ :POST send a post request using a country name to add it's country code """

    def post(self): 
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('country_name', type=str, required=True, help="Country name as string, cant be blank", location='args')
        parser.add_argument('country_code', type=int, required=True, help="Country code as int, cant be blank", location='args')
        args = parser.parse_args()

        name = args["country_name"]
        code = args["country_code"]

        result = db.adding_country_code_db(country_name=name, country_code=code)

        return result
api.add_resource(add_country_code, '/add_country_code')

class adding_country_iso_code(Resource):
    """ :POST send a post request using a country name to add it's iso code """
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('country_name', type=str, required=True, help="Country name as string, cant be blank", location='args')
        parser.add_argument('iso_code', type=str, required=True, help="Country iso code as string, cant be blank", location='args')
        args = parser.parse_args()

        name = args["country_name"]
        code = args["iso_code"]

        result = db.adding_iso_code(country_name=name, iso_code=code)
        return result
api.add_resource(adding_country_iso_code, '/add_country_iso_code')

class add_country_fun_fact(Resource):
    """ :POST: send a post request using a country name to add it's fun fact """
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('country_name', type=str, required=True, help="Country name as string, cant be blank", location='args')
        parser.add_argument('fun_fact', type=str, required=True, help="Country fun string 250 and less character, cant be blank", location='args')
        args = parser.parse_args()

        name = args["country_name"]
        fact = args["fun_fact"]

        result = db.add_fun_fact(country_name=name, fun_fact=fact)

        return result
api.add_resource(add_country_fun_fact, "/add_fun_fact")


## PUT endpoint ## PUT endpoint 

class edit_fun_facts(Resource):
    """ :PUT: send put request  """
    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('country_name', type=str, required=True, help="Country name as string, cant be blank", location='args')
        parser.add_argument('new_fun_fact', type=str, required=True, help="Country fun string 250 and less character, cant be blank", location='args')
        args = parser.parse_args()

        name = args["country_name"]
        new_fact = args["new_fun_fact"]       

        result = db.edit_fun_fact(country_name=name, new_fact=new_fact)

        return result
api.add_resource(edit_fun_facts, "/edit_fun_fact")