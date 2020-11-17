from pymongo import MongoClient
from datetime import datetime

import pymongo

# go to server folder and enter (mongod --dbpath=data) to start the server


# Connecting to the mongodb
port = int(input("Enter a port number: "))
client = MongoClient('localhost', port)

# creating a database
db = client['291db']
print("Database \'291db\' is created !!")

postsCol = db['Posts']
votesCol = db['Votes']
postsCol.create_index([('Title', pymongo.TEXT), ('Body', pymongo.TEXT), ('Tags', pymongo.TEXT)], name='search_index', default_language='english')

userInputId = input("Enter your ID: ")

if userInputId:
    postsId = []
    # Average for questions
    sum = 0;
    counter = 0;
    results = postsCol.find({ "OwnerUserId":userInputId, "PostTypeId":"1"})  # "1" are Questions and "2" are Answers
    for result in results:
        postsId.append(result["Id"])
        counter += 1
        sum += int(result["Score"])
    print("The number of questions owned: ", counter)
    print("The average score for questions is: ", sum/counter)

    # Average for answers
    sum = 0;
    counter = 0;
    results = postsCol.find({ "OwnerUserId":userInputId, "PostTypeId":"2"})  # "1" are Questions and "2" are Answers
    for result in results:
        postsId.append(result["Id"])
        counter += 1
        sum += int(result["Score"])
    print("The number of answers owned: ", counter)
    print("The average score for answers is: ", sum/counter)

    # Number of votes registered for the user
    counter = 0
    results = votesCol.find({})
    for result in results:
        if result["PostId"] in postsId:
            counter += 1
    print("Number of votes registered for the user is: ", counter)



# Second Part
run = True
while run:
    userAction = input("Posts question(Enter 1), Search for questions(Enter 2): ")
    if userAction == '1':
        # Posts question
        # postsCol.create_index( { "Id":1}, unique = True)
        titleText = input("Enter Title: ")
        bodyText = input("Enter Body: ")

        # Getting the tags
        tagNumber = input("Enter the number of tags: ")
        tagText = ""
        for i in range(int(tagNumber)):
            tagText = tagText + "<" + input("Enter a tag: ") + ">"

        # Creation Date
        s = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')

        # missing Id, and havn't handle if no OwnerUserId
        postsCol.insert_one({"PostTypeId": "1",
                            "Title": titleText,
                            "Body": bodyText,
                            "Tags": tagText,
                            "CreationDate": s[:-3],
                            "OwnerUserId": userInputId,
                            "Score": 0,
                            "ViewCount": 0,
                            "AnswerCount": 0,
                            "CommentCount": 0,
                            "FavoriteCount": 0,
                            "ContentLicense": "CC BY-SA 2.5"})
        print("Your question is posted!")
        # Ending the program      
        if input("Do you want to end the program?(y/n) ") == "y":
            print("Ending the program...")
            run = False

    elif userAction == '2':
        pass
        # Search for questions
        keyWords = input("Enter keywords seperated by space: ")
        results = postsCol.find({"$text": {"$search": keyWords, "$caseSensitive": False}, "PostTypeId": "1"})
        for result in results:
    
            # printing each question
            print("Title: ", result["Title"])
            print("Creation Date: ", result["CreationDate"])
            print("Score: ", result["Score"])
            print("Answer Count: ", result["AnswerCount"])

            # user selecting a question
            if input("Select this question?(y/n) ") == "y":
                
                print(result)
                postsCol.update_one({"_id": result["_id"]}, {"$inc": {"ViewCount": 1 }})
                print("ViewCount has been incremented.")

                userQuestionAction = input("Do you want to Answer the question or view all the answer from this question:(answer/view) ")
                if userQuestionAction == "answer":
                    answerBody = input("Enter the body of your answer: ")

                    # Creation Date
                    s = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')

                    # ParentId, OwnerUserID and Id may be missing
                    postsCol.insert_one({"Body": answerBody,
                                        "PostTypeId": "2",
                                        "CreationDate": s[:-3],
                                        "OwnerUserId": userInputId,
                                        "ParentId": result["Id"],
                                        "Score": 0,
                                        "CommentCount": 0,
                                        "ContentLicense": "CC BY-SA 2.5"
                                        })
                    print("Answer posted!")
                    if input("Do you want to view all the answer for this question?(y/n) ") == 'y': userQuestionAction = "view"

                if userQuestionAction == "view":
                    # Task 4
                    pass




                break;
        

