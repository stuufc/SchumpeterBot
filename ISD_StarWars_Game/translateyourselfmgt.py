import random
import json
from apimanagement import *
from guessquotemgt import GetRandomStarwarsQuote
from usermanagement import AddPointsForUser
yodaanswerforquote = ''
solution_showed = False

#Function "ShowQuoteToTranslate" gets a random Quote from the DB and sends it to the API for the solution. The Original is showed to the user for translation
def ShowQuoteToTranslate():
    global solution_showed
    solution_showed = False
    with open("starwars_quotes.json", "r") as file:
        data = json.load(file)
    random_record = random.choice(data)
    translated_quote = GetYodaQuote(random_record["quote"])
    SetGlobalAnswer(translated_quote, False)
    return ("Translate the Following Quote: " + random_record["quote"])
    
#Function "SetGlobalAnswer" defines the answer quote which was loaded in the function ShowQuoteToTranslate or resets the answer. It is neccessary to check the answer.
def SetGlobalAnswer(yodaanswer, is_reset):
    global yodaanswerforquote
    if is_reset:
        yodaanswerforquote = ''
    else:
        yodaanswerforquote = yodaanswer

#Function "CheckAnswerFromUser" compares the user answer with the answer from the API. Points are awarded if the answer is correct.       
def CheckAnswerFromUser(username, useranswer):
    global solution_showed
    if solution_showed == True:
        return "Error: The solution for this quote has already been showed. Please try another one."
    if useranswer == yodaanswerforquote:
        AddPointsForUser(username,1)
        userfeedback= "Congratulations. The sentence has been translated correctly."
    else:
        userfeedback = "Unfortunately, the sentence was not translated correctly. Good luck with your next attempt."    
    SetGlobalAnswer(yodaanswerforquote, True)
    return(userfeedback)

#Function "ShowSolution" shows the Solution to the User if a quote is loaded.
def ShowSolution():
    global yodaanswerforquote
    if yodaanswerforquote != '':
        global solution_showed
        solution_showed = True
        return yodaanswerforquote
    else:
        return "Error: No solution to show at the moment."