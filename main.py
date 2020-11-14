import pymongo, json
from pymongo import MongoClient


# go to server folder and enter (mongod --dbpath=data) to start the server

# Connecting to the mongodb
port = int(input("Enter a port number: "))
client = MongoClient('localhost', port)

# creating a database
db = client['291db']
print("Database \'291db\' is created !!")

# remove already exist collections
collectionToRemove = ["Posts", "Tags", "Votes"]
for collection in db.list_collection_names():
    if collection in collectionToRemove:
        db[collection].drop()

# creating a collection
col = db["Posts"]

# # inserting data into mongodb
with open("Posts.json") as file:
    file_data = json.load(file)

if isinstance(file_data, list):
    col.insert_many(file_data)
else:
    col.insert_one(file_data)



