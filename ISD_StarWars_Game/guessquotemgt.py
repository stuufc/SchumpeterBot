import json
import random
from apimanagement import *
from usermanagement import AddPointsForUser
global_quote = {}
hint_claimed = False
solution_showed = False

#Function "GetRandomStarwarsQuote" loads a random Quote from the Database and sends it to the API for the Translation
def GetRandomStarwarsQuote():
    global solution_showed
    solution_showed = False
    with open("../starwars_quotes.json", "r") as file:
        data = json.load(file)
        
    random_record = random.choice(data)
    SetGlobalQuote(random_record, False)
    translated_random_quote = GetYodaQuote(random_record["quote"])
    return random_record, translated_random_quote

#Function "SetGlobalQuote" defines the random quote which was loaded in the function GetRandomStarwarsQuote or resets the answer. It is neccessary to check the answer.
def SetGlobalQuote(random_record, is_reset):
    global global_quote
    if is_reset:
        global_quote = {}
    else:
        global_quote = random_record

#Function "SetHint" sets the Global Variable if the User has claimed a hint
def SetHint(is_Reset):
    global hint_claimed
    if is_Reset:
        hint_claimed = False
    else:
        hint_claimed = True

#Function "IsActorNumberInJson" checks if the Number from the User is in the Database File
def IsActorNumberInJson(actor_number):
    with open("../characters.json", "r") as file:
        data = json.load(file)
        
    return any(entry["Nr."] == actor_number for entry in data)

#Function "CheckAnswerForSaidBy" Compares the Globally Said By Variable with the User Answer
def CheckAnswerForSaidBy(useranswer, username):

    global global_quote, hint_claimed, solution_showed

    #check if there is a quote to compare with
    if not isinstance(global_quote, dict) or not global_quote:
        return "Error: No Quote to proof Error. The Yoda Sentence was not created."

    #check if the solution has already been shown
    if solution_showed:
        return "Error: The solution has been showed for this translation. Please try another one."

    #Get the Actor with the useranswer
    if IsActorNumberInJson(useranswer):
        with open("../characters.json", "r") as file:
            data = json.load(file)
        for entry in data:
            if entry["Nr."] == useranswer:
                useranswer_said_by = entry["Character_Name"]
    else:
        return "The number given is invalid or does not match any actor. Please check the list"
        
    #compare the user's guess with the actual quote

    if 'said_by' in global_quote and global_quote['said_by'] == useranswer_said_by:
        if hint_claimed:
            AddPointsForUser(username, 0.5)
        else:
            AddPointsForUser(username, 1)

        #set the flag indicating the solution has been shown
        solution_showed = True

        #reset the global quote and hint flag for a new game
        SetGlobalQuote({}, True)
        SetHint(True)

        return "Congratulations. The answer was right. The points will be added to your user."

    else:
        #response for an incorrect guess, do not reset the global quote
        return "Unfortunately, the answer was wrong. You may have another guess."

    
#Function "ClaimeHint" Gets the Movie from the Quote and provides it to the user    
def ClaimHint():
    SetHint(False)
    return("The movie in which the sentence appeared was: " + global_quote["movie"])

#Function "ShowSolution" Shows the Solution from the actual question
def ShowSolution():
    global global_quote
    if global_quote["said_by"] != '':
        global solution_showed
        solution_showed = True
        return global_quote["said_by"]
    else:
        return "Error: No solution to show at the moment."
    
#Function "GetAllActors" Gets all Actors from the Database and provide it to the user
def GetAllActors():
    with open("../characters.json", "r") as file:
        data = json.load(file)
        
    actor_list = [(entry['Nr.'], entry['Character_Name']) for entry in data]

    return actor_list