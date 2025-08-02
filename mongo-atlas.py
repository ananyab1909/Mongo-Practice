

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<username>:<password>@cluster0.qjvts7o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'),connectTimeoutMS=60000)

def connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def dbcreate():
    try:
        name=input("Enter db name: ")
        db_names = client.list_database_names()
        if name not in db_names:
            db = client[name]
            print("Database created:", db.name)
            return db
        else:
            print("Database already exists.")
            return client[name]
    except Exception as e:
        print(e)

def collectcreate(db):
    try:
        name=input("Enter collection name: ")
        db = client[name]
        collection_names = db.list_collection_names()
        if name not in collection_names:
            collection = db[name]
            print("Collection created:", collection.name)
            return collection
        else:
            print("Collection already exists.")
            return db[name]
    except Exception as e:
        print(e)
        return None

def user_input():
    num_col = int(input("How many columns do you want to insert? "))
    columns = []
    for i in range(num_col):
        column_name = input(f"Enter name for column {i+1}: ")
        columns.append(column_name)
    num_doc = int(input("How much data do you want to insert? "))
    data = []
    for i in range(num_doc):
        document = {}
        for column in columns:
            value = input(f"Enter {column} for document {i+1}: ")
            document[column] = value
        data.append(document)   
    return data, columns

def insert_docs(collection, data, columns):
    try:
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents.")
    except Exception as e:
        print(e)

def dbinsert(db):
    collection = collectcreate(db)
    if collection is not None:
        data, columns = user_input()
        insert_docs(collection, data, columns)
    else:
        print("Failed to create or retrieve the collection.")

def delete_docs(collection):
    try:
        choice = input("Do you want to delete one or many documents? (one/many): ")
        if choice.lower() == "one":
            column_name = input("Enter the column name: ")
            column_value = input("Enter the column value: ")
            filter = {column_name: column_value}
            result = collection.delete_one(filter)
            print(f"Deleted {result.deleted_count} document.")
        elif choice.lower() == "many":
            column_name = input("Enter the column name: ")
            column_value = input("Enter the column value: ")
            filter = {column_name: column_value}
            result = collection.delete_many(filter)
            print(f"Deleted {result.deleted_count} documents.")
        else:
            print("Invalid choice. Please enter 'one' or 'many'.")
    except Exception as e:
        print(e)

def dbdelete():
    print("Deleting documents")
    collection = collectcreate(db)
    if collection is not None:
        delete_docs(collection)
    else:
        print("Failed to create or retrieve the collection.")

def update_doc(collection):
    print("Updating data")
    try:
        column_name = input("Enter the column name to update: ")
        column_value = input("Enter the column value to update: ")
        new_value = input("Enter the new value: ")
        filter = {column_name: column_value}
        update = {"$set": {column_name: new_value}}
        result = collection.update_one(filter, update)
        print(f"Updated {result.matched_count} document.")
    except Exception as e:
        print(e)

def showdata(db):
    print("Showing the data")
    collection = collectcreate(db)
    if collection is not None:
        try:
            results = collection.find()
            for result in results:
                print(result)
        except Exception as e:
            print(e)
    else:
        print("Failed to create or retrieve the collection.")


connection()
db = dbcreate()
dbinsert(db)
showdata(db)
dbdelete()
showdata(db)

collection = collectcreate(db)
update_doc(collection)
showdata(collection)
