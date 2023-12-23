import json
import random
from apimanagement import *
from usermanagement import AddPointsForUser
global_quote_said_by = ''

#Function GetRandomStarwarsQuote loads a random Quote from the Database and sends it to the API for the Translation
def GetRandomStarwarsQuote():
    with open("starwars_quotes.json", "r") as file:
        data = json.load(file)
        
    random_record = random.choice(data)
    SetGlobalQuote(random_record["said_by"], False)
    random_quote = random_record["quote"]
    translated_random_quote = GetYodaQuote(random_quote)
    return(translated_random_quote)

#Function SetGlobalQuote defines the random quote which was loaded in the function GetRandomStarwarsQuote or resets the answer. It is neccessary to check the answer.
def SetGlobalQuote(said_by, is_reset):
    global global_quote_said_by
    if is_reset:
        global_quote_said_by == ''
    else:
        global_quote_said_by == said_by

#Function CheckAnswerForSaidBy
def CheckAnswerForSaidBy(useranswer, username):
    if global_quote_said_by == '':
        AddPointsForUser(username,1)
        return("Error: No Quote to proof Error. The Yoda Sentence was not created.")
    
    if global_quote_said_by == useranswer:
        return("Congratulations. The Answer was right. They points will be added to your user.")
    else:
        return("Unfortunately, the answer was wrong. Good luck next time.")
    
    
    

    
        