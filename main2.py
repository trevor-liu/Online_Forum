# search function return post without keywords

from pymongo import MongoClient
from datetime import datetime
import random, re, pymongo

# go to server folder and enter (mongod --dbpath=data) to start the server



# Connecting to the mongodb
port = int(input("Enter a port number: "))
client = MongoClient('localhost', port)

# creating a database
db = client['291db']
print("Database \'291db\' is created !!")

postsCol = db['Posts']
tagsCol = db["Tags"]
votesCol = db['Votes']
db["Posts"].create_index([('Title', pymongo.TEXT), ('Body', pymongo.TEXT), ('Tags', pymongo.TEXT)], name='search_index')



# Creating a unique post Id
def uniquePid():
    uniqueId = ""
    notFinished = True
    while (notFinished):
        uniqueId = str(random.randint(400700, 1000000000))
        if postsCol.count_documents({'Id': uniqueId}) <= 0:
            notFinished = False
    return uniqueId


# Creating a unique post Id
def uniqueVid():
    uniqueId = ""
    notFinished = True
    while (notFinished):
        uniqueId = str(random.randint(0, 1000000000))
        if votesCol.count_documents({'Id': uniqueId}) <= 0:
            notFinished = False
    return uniqueId

# Creating a unique post Id
def uniqueTid():
    uniqueId = ""
    notFinished = True
    while (notFinished):
        uniqueId = str(random.randint(0, 1000000000))
        if tagsCol.count_documents({'Id': uniqueId}) <= 0:
            notFinished = False
    return uniqueId

def checkTag(tagText):

    tagText = re.findall(r"[\w']+", tagText)

    for i in tagText:
        if tagsCol.count_documents({"TagName": i}) > 0:
            tagsCol.update_one({"TagName": i}, {"$inc": {"Count": 1}})
        else:
            tagsCol.insert_one({"Id": uniqueTid(), "TagName": i, "Count": 1})


userInputId = input("Enter your ID: ")

# record vote into the system
# return True if vote are valid, False if it is invalid
def votingOnPost(post_Id, vote_type):

    # check if user already voted in the same post
    if userInputId is not "" and votesCol.count_documents({"PostId": post_Id, "userId": userInputId}) is not 0: return False

    # Creation Date
    s = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')
    votesCol.insert_one({"PostId": post_Id, "userId": userInputId, "VoteTypeId": "2", "CreationDate": s[:-3], "Id": uniqueVid()}) # create Unique Id

    return True


if userInputId:
    postsId = []

    # Average for questions
    sum = 0
    counter = 0
    results = postsCol.find({ "OwnerUserId":userInputId, "PostTypeId":"1"})  # "1" are Questions and "2" are Answers
    for result in results:
        postsId.append(result["Id"])
        counter += 1
        sum += int(result["Score"])
    print("The number of questions owned: ", counter)
    print("The average score for questions is: ", round(sum/counter, 2))

    # Average for answers
    sum = 0
    counter = 0
    results = postsCol.find({ "OwnerUserId":userInputId, "PostTypeId":"2"})  # "1" are Questions and "2" are Answers
    for result in results:
        postsId.append(result["Id"])
        counter += 1
        sum += int(result["Score"])
    print("The number of answers owned: ", counter)
    print("The average score for answers is: ", round(sum/counter, 2))

    # Number of votes registered for the user
    counter = votesCol.count_documents({"userId": userInputId})
    print("Number of votes registered for the user is: ", counter)



# Second Part
run = True
while run:
    userAction = input("Posts question(Enter 1), Search for questions(Enter 2), or Exit(Enter 3): ")
    if userAction == "3": run = False
    elif userAction == '1':
        # Posts question
        titleText = input("Enter Title: ")
        bodyText = input("Enter Body: ")

        # Getting the tags
        tagNumber = input("Enter the number of tags: ")
        tagText = ""
        for i in range(int(tagNumber)):
            tagText = tagText + "<" + input("Enter a tag: ") + ">"

        checkTag(tagText)
        # Creation Date
        s = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')


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
                            "Id": uniquePid(),
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
        print("The number of Question that have this keywords: ",  postsCol.count_documents({"$text": {"$search": keyWords, "$caseSensitive": False}, "PostTypeId": "1"}))

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

                userQuestionAnswerAction = input("Do you want to Answer the question, view all the answer, or vote on this question?(answer/view/vote) ")
                if userQuestionAnswerAction == "answer":
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
                                        "ContentLicense": "CC BY-SA 2.5",
                                        "Id": uniquePid()
                                        })
                    postsCol.update_one({"Id": result["Id"]}, {"$inc": {"AnswerCount": 1}})
                    print("Answer posted!")

                if userQuestionAnswerAction == "view":
                    # Task 4

                    # if there are accepted answer, display accepted answer first than all answer
                    # else just display all answer
                    if "AcceptedAnswerId" in result:
                        acceptedAnswer = postsCol.find_one({"Id": result["AcceptedAnswerId"]})
                        print("Body: ", acceptedAnswer["Body"][:80])
                        print("CreationDate: ", acceptedAnswer["CreationDate"])
                        print("Score: ", acceptedAnswer["Score"])
                        if input("Do you want to select this answer?(y/n) ") == "y":
                            selectedAnswer = acceptedAnswer
                            answerSeleted = True
                            print(selectedAnswer)
                            if input("Do you want to vote on this answer?(y/n) ") == "y": userQuestionAnswerAction = "vote"
                            break

                        allAcceptedAnswer = postsCol.find({"ParentId": result["Id"], "Id": {"$nin": [result["AcceptedAnswerId"]]} })
                        for answer in allAcceptedAnswer:
                            print("Body: ", answer["Body"][:80])
                            print("CreationDate: ", answer["CreationDate"])
                            print("Score: ", answer["Score"])
                            if input("Do you want to select this answer?(y/n) ") == "y":
                                selectedAnswer = answer
                                answerSeleted = True
                                print(selectedAnswer)
                                if input("Do you want to vote on this answer?(y/n) ") == "y": userQuestionAnswerAction = "vote"
                                break
                    else:
                        allAcceptedAnswer = postsCol.find({"ParentId": result["Id"]})
                        for answer in allAcceptedAnswer:
                            print("Body: ", answer["Body"][:80])
                            print("CreationDate: ", answer["CreationDate"])
                            print("Score: ", answer["Score"])
                            if input("Do you want to select this answer?(y/n) ") == "y": 
                                selectedAnswer = answer
                                answerSeleted = True
                                print(selectedAnswer)
                                if input("Do you want to vote on this answer?(y/n) ") == "y": userQuestionAnswerAction = "vote"
                                break
                    
                    
                # Voting on the selected post
                if userQuestionAnswerAction == "vote" and answerSeleted and votingOnPost(selectedAnswer["Id"], "2"):
                    # increase the score by one
                    postsCol.update_one({"Id": selectedAnswer["Id"]}, {"$inc": {"Score": 1}})

                elif userQuestionAnswerAction == "vote" and votingOnPost(result["Id"], "2"):
                    postsCol.update_one({"Id": result["Id"]}, {"$inc": {"Score": 1}})
                        


                # check if the user want to exit the program after 2-5
                if input("Do you want to exit the the program?(y/n) ") == "y": run = False
                
                





                break           # after the user selected a question, stop displaying all the remaining post

