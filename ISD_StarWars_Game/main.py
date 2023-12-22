import json
import requests

#Function "LoginPlayer": This function Logs in the User for the Star Wars Game
def LoginPlayer():
    #Mask for the User Login
    username = input("Please give in your username: ")
    password = input("Please give in your password: ")
    
    #Check the Password and Welcome the User if correct
    if FindUser(username):
        expected_password = FindUser(username)[1]
        if password == expected_password:
            print("Welcome to the Starwars game "+ username)
        else:
            print("Invalid Password. Please try again.")
            return
    else: 
        print("User not found. Please try again!")
        return
    
#Function "CreatePlayer": This function Register a new Player for the Star Wars Game
def CreatePlayer():
    #User Input for Username and Password also check user name
    username = input("Create a username: ")
    password = input("Create a password for this new user: ")
    if FindUser(username):
        print("The User you want to create already exists. Please select another name")
        return
    
    #Check if a database exists and load the database file. If not a empty data set is created
    try:
        with open("user_database.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    
    #The new player is added into the database file    
    player_data = {"username": username, "password": password}
    data.append(player_data)
    with open("user_database.json", "w") as file:
        json.dump(data, file, indent=2)
                
    return username
    
#Function "CheckUser": This functions proofs if the user already exists in our database    
def FindUser(username_to_proof):
    try:
        #Read the actual User Database
        with open("user_database.json", "r") as file:
            data = json.load(file)
        #Iterate through the Database and look for an existing user
        for username in data:
            if username["username"] == username_to_proof:
                return username["username"], username["password"]
    except FileNotFoundError:
        pass
    return False

#Function "GetYodaQuote": To Get the Yoda Quote from the API    
def GetYodaQuote(SentenceToTranslate):
    #Create API Call
    request_url = "https://api.funtranslations.com/translate/yoda.json?text="
        
    #Call the API
    response = requests.get(request_url+SentenceToTranslate)
    
    #Read Out the Translated Sentence if ther is an Answer and Give it Back
    if response.status_code == 200:
        api_data = response.json()
        yoda_text = api_data['contents']['translated']        
        if yoda_text != '':
            return(yoda_text)
        else:
            return("The text could not be translated or was empty.")
    else:
        print("API Error")

CreatePlayer()
#LoginPlayer()
#print(GetYodaQuote("This is a Test Sentence to call the API"))
