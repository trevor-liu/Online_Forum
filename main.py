# Phase 1
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

# inserting Posts data into mongodb
with open("Posts.json") as file:
    file_data = json.load(file)

col.insert_many(file_data["posts"]["row"][::2])
col.insert_many(file_data["posts"]["row"][1::2])

# creating a collection
col = db["Tags"]

# inserting Posts data into mongodb
with open("Tags.json") as file:
    file_data = json.load(file)


col.insert_many(file_data["tags"]["row"][::2])
col.insert_many(file_data["tags"]["row"][1::2])


# creating a collection
col = db["Votes"]

# inserting Posts data into mongodb
with open("Votes.json") as file:
    file_data = json.load(file)

col.insert_many(file_data["votes"]["row"][::2])
col.insert_many(file_data["votes"]["row"][1::2])