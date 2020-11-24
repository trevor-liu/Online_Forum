from pymongo import MongoClient
from datetime import datetime
import random

import pymongo

# go to server folder and enter (mongod --dbpath=data) to start the server



# Creating a unique post Id
def uniqueId():
    uniqueId = ""
    notFinished = True
    while (notFinished):
        uniqueId = str(random.randint(400700, 1000000))
        if postsCol.count_documents({'Id': uniqueId}) <= 0:
            notFinished = False
    print(uniqueId)
    return uniqueId




# Connecting to the mongodb
port = int(input("Enter a port number: "))
client = MongoClient('localhost', port)

# creating a database
db = client['291db']
print("Database \'291db\' is created !!")

postsCol = db['Posts']
tagsCol = db["Tags"]
votesCol = db['Votes']

userInputId = input("Enter your ID: ")

# record vote into the system
def votingOnPost(post_Id, vote_type):
    # Creation Date
    s = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')

    # check if user already voted in the same post
    if userInputId:
        votesCol.find_one({"PostId": post_Id})
        pass
    else:
        votesCol.insert_one({"PostId": post_Id, "VoteTypeId": "2", "CreationDate": s[:-3]})  # create Unique Id

    return True


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
                            "Id": uniqueId(),
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

                selectedAnswer = {}
                answerSeleted = False
                print(result)
                postsCol.update_one({"_id": result["_id"]}, {"$inc": {"ViewCount": 1 }})

                userQuestionAction = input("Do you want to Answer the question, view all the answer, or vote on this question?(answer/view/vote) ")
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

                if userQuestionAction == "view":
                    # Task 4

                    # if there are accepted answer, display accepted answer first than all answer
                    # else just display all answer
                    if "AcceptedAnswerId" in result:
                        acceptedAnswer = postsCol.find_one({"Id": result["AcceptedAnswerId"]})
                        print(acceptedAnswer["Body"][:80])
                        print(acceptedAnswer["CreationDate"])
                        print(acceptedAnswer["Score"])
                        if input("Do you want to select this answer?(y/n) ") == "y":
                            selectedAnswer = acceptedAnswer
                            answerSeleted = True
                            print(selectedAnswer)
                            break

                        allAcceptedAnswer = postsCol.find({"ParentId": result["Id"], "Id": {"$nin": [result["AcceptedAnswerId"]]} })
                        for answer in allAcceptedAnswer:
                            print(answer["Body"][:80])
                            print(answer["CreationDate"])
                            print(answer["Score"])
                            if input("Do you want to select this answer?(y/n) ") == "y":
                                selectedAnswer = answer
                                answerSeleted = True
                                print(selectedAnswer)
                                break
                    else:
                        allAcceptedAnswer = postsCol.find({"ParentId": result["Id"]})
                        for answer in allAcceptedAnswer:
                            print(answer["Body"][:80])
                            print(answer["CreationDate"])
                            print(answer["Score"])
                            if input("Do you want to select this answer?(y/n) ") == "y": 
                                selectedAnswer = answer
                                answerSeleted = True
                                print(selectedAnswer)
                                break
                    
                    
                # Voting on the selected post
                if userQuestionAction == "vote" and answerSeleted and votingOnPost(selectedAnswer["Id"], "2"):
                    # increase the score by one
                    pass
                elif userQuestionAction == "vote" and votingOnPost(result["Id"], "2"):
                    # increase the score by one
                    pass
                        


                # check if the user want to exit the program after 2-5
                if input("Do you want to exit the the program?(y/n) ") == "y": run = False
                
                





                break           # after the user selected a question, stop displaying all the remaining post
        


