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
    with open("starwars_quotes.json", "r") as file:
        data = json.load(file)
        
    random_record = random.choice(data)
    SetGlobalQuote(random_record, False)
    translated_random_quote = GetYodaQuote(random_record["quote"])
    return(translated_random_quote)

#Function "SetGlobalQuote" defines the random quote which was loaded in the function GetRandomStarwarsQuote or resets the answer. It is neccessary to check the answer.
def SetGlobalQuote(random_record, is_reset):
    global global_quote
    if is_reset:
        global_quote = ''
    else:
        global_quote = random_record

#Function "SetHint" sets the Global Variable if the User has claimed a hint
def SetHint(is_Reset):
    global hint_claimed
    if is_Reset:
        hint_claimed = False
    else:
        hint_claimed = True

#Function "CheckAnswerForSaidBy" Compares the Globally Said By Variable with the User Answer
def CheckAnswerForSaidBy(useranswer, username):
    if global_quote == {}:
        return("Error: No Quote to proof Error. The Yoda Sentence was not created.")
    
    if solution_showed == True:
        return("Error: The solution has been showed for this translation. Please try another one.")
    
    if global_quote["said_by"] == useranswer:
        if hint_claimed:
            AddPointsForUser(username,0.5)
        else:
            AddPointsForUser(username,1)
        user_feedback ="Congratulations. The Answer was right. They points will be added to your user."
    else:
        user_feedback = "Unfortunately, the answer was wrong. Good luck next time."
    
    SetGlobalQuote({},True)
    SetHint(True)
    return(user_feedback)
    
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