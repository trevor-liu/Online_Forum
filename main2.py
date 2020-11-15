from pymongo import MongoClient

# go to server folder and enter (mongod --dbpath=data) to start the server

# Connecting to the mongodb
port = int(input("Enter a port number: "))
client = MongoClient('localhost', port)

# creating a database
db = client['291db']
print("Database \'291db\' is created !!")

postsCol = db['Posts']
votesCol = db['Votes']

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
    userAction = input("Posts question(Enter 1), Search for questions(Enter 2), Question action-Answer(Enter 3), Question action_List answers(Enter 4), Question/Answer action-Vote(Enter 5). Enter 0 to end the program: ")
    if userAction == '0':
        print("Ending the program...")
        run = False
    elif userAction == '1':
        # Posts question
        # postsCol.create_index( { "Id":1}, unique = True)
        # titleText = input("Enter Title: ")
        # bodyText = input("Enter Body: ")
        # tagText = input("Enter tags: ")
        # postsCol.insert_one({ "PostTypeId": "1",
        #                     "Title": titleText, 
        #                     "Body": bodyText,
        #                     "Tags": tagText})


        pass
    elif userAction == '2':
        # Search for questions

        pass
    elif userAction == '3':
        # Question action-Answer

        pass
    elif userAction == '4':
        # Question action_List answers

        pass
    elif userAction == '5':
        # Question/Answer action-Vote

        pass