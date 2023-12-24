import json

#Function "AddPointsForUser" handles the Usermanagement and is called by the games
def AddPointsForUser(username, amountofpoints):
    if FindUser(username):
        newamountofpoints = int(FindUser(username)[2]) + amountofpoints
        id_to_update = FindUser(username)[0]
        UpdateUserWithNewPoints(id_to_update, username, newamountofpoints)
    else:
        CreateUserForGame(username, amountofpoints)
        

#Function "CheckUser": This functions proofs if the user already exists in our database    
def FindUser(username_to_proof):
    try:
        #Read the actual User Database
        with open("user_database.json", "r") as file:
            data = json.load(file)
        #Iterate through the Database and look for an existing user
        for username in data:
            if username["username"] == username_to_proof:
                return username["id"], username["username"], username["points"]
    except FileNotFoundError:
        pass
    return False 

# Function "CreateUserForGame" creates the user in our database and adds the points they've scored.
def CreateUserForGame(username, amountofpoints):
    # Check if a database exists and load the database file. If not, an empty dataset is created.
    try:
        with open("user_database.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    # Find the last ID and increment it by one
    last_id = 0
    if data:
        last_id = max(item.get("id", 0) for item in data)

    # The new player is added to the database file with the incremented ID
    player_data = {"id": last_id + 1, "username": username, "points": amountofpoints}
    data.append(player_data)
    
    # Save the updated data back to the database file
    with open("user_database.json", "w") as file:
        json.dump(data, file, indent=2)

#Function "UpdateUserWithNewPoints" adds the new amount of Points to the user in the Database
def UpdateUserWithNewPoints(id, username, newamountofpoints):
    newrecord = {"username": username, "points": newamountofpoints}
    with open("user_database.json", 'r') as file:
        data = json.load(file)

    for datarecord in data:
        if datarecord["ID"] == id:
            datarecord.update(newrecord)
            break

    with open("user_database.json", 'w') as file:
        json.dump(data, file, indent=2)
        
#Function "ShowStatisticsForUser" returns the actual amount of points for the user
def ShowStatisticsForUser(username):
    if int(FindUser(username)[2]) > 0:
        return "Player " + username + "has " + (FindUser(username)[2]) + " points at the moment."
    else:
        return "Player " + username + "has 0 points at the moment."