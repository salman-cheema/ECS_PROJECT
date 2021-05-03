from flask import Flask
from flask import request
from flask import jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import datetime
import os
import config as config
# connect to MongoDB, change the \
# << MONGODB URL >> to reflect your own connection string


app = Flask(__name__)
mongo = os.environ['mongo']
client = MongoClient(str(mongo)+str(config.MONGO_CONNECTION))

@app.route('/')
def hello():
    return str(" WELCOME TO FLASK APPLICATION DEPLOYED ON ECS THROUGH CODEPIPELINE CHANGED")
@app.route('/insert')
def insert():
    mydb = client["mydatabase"]
    mycol = mydb["customers"]
    mydict = { "name": "John", "address": "Highway 37" }
    x = mycol.insert_one(mydict)
    databases = client.list_database_names()
    for database in databases:
        # databases
        pprint("database::" + str(database))
    return ('DATA INSERTED \n:: STATUS CODE::200')


@app.route('/get-data')
def get():
    data_list = []
    mydb = client["mydatabase"]
    mycol = mydb["customers"]
    myquery = {"address":"Highway 37"}
    mydoc = mycol.find(myquery)
    for data in mydoc:
        data['_id'] = str(data['_id'])
        data_list.append(data)
        
    resp = {'dataa': data_list}
    return jsonify(resp)
    


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5011',debug=True)
