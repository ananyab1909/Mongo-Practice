from flask import Flask,jsonify
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)

name = input("Enter name of database:")
uri = "mongodb://127.0.0.1:27017/" + name

app.config["MONGO_URI"] = uri
mongo = PyMongo(app)

if mongo.cx:
    print("Connected to MongoDB!")
else:
    print("Failed to connect!")

print("Connected to database:", mongo.db.name)

collection = input("Enter name of collection:")
mongo.db.create_collection(collection)
print(f"Collection '{collection}' created successfully!")
my_collection = mongo.db[collection]
print("Collection ready to use")

def user_input():
    num_col = int(input("How many columns do you want to insert? "))
    columns = []
    for i in range(num_col):
        column_name = input(f"Enter name for column {i+1}: ")
        columns.append(column_name)
    num_doc = int(input("How much data do you want to insert? "))
    data = []
    for i in range(num_doc):
        document = []
        for column in columns:
            value = input(f"Enter {column} for document {i+1}: ")
            document.append(value)
        data.append(document)   
    return data, columns

data, columns = user_input()

@app.route('/insert', methods=['POST'])
def insert() :
    data_json = []
    for doc in data:
        doc_json = {}
        for i, column in enumerate(columns):
            doc_json[column] = doc[i]
        data_json.append(doc_json)
    my_collection.insert_many(data_json)
    return jsonify({'message': 'Data inserted successfully'}),200

@app.route('/data', methods=['GET'])
def get_data():
    data = my_collection.find()
    return jsonify(json_util.dumps(data)), 200

if __name__ == '__main__':
    app.run(debug=False)




    
    
