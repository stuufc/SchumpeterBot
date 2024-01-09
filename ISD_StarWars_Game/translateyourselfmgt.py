import random
import json
import re
from apimanagement import *
from guessquotemgt import GetRandomStarwarsQuote
from usermanagement import AddPointsForUser
yodaanswerforquote = ''
solution_showed = False

#Function "ShowQuoteToTranslate" gets a random Quote from the DB and sends it to the API for the solution. The Original is showed to the user for translation
def ShowQuoteToTranslate():
    global solution_showed
    solution_showed = False
    with open("../starwars_quotes.json", "r") as file:
        data = json.load(file)
    random_record = random.choice(data)
    translated_quote = GetYodaQuote(random_record["quote"])
    SetGlobalAnswer(translated_quote, False)
    return random_record["quote"], translated_quote

#Function "SetGlobalAnswer" defines the answer quote which was loaded in the function ShowQuoteToTranslate or resets the answer. It is neccessary to check the answer.
def SetGlobalAnswer(yodaanswer, is_reset):
    global yodaanswerforquote
    if is_reset:
        yodaanswerforquote = ''
    else:
        yodaanswerforquote = yodaanswer

#function to standardize the strings to make it easier to compare them
def NormalizeQuote(quote):
    #remove spaces and convert to lowercase
    quote_no_spaces = re.sub(r"\s+", "", quote).lower()

    #standardize apostrophes by replacing it with a standard one. Method from re-module is used
    normalized_quote = re.sub(r"[’'`]", "'", quote_no_spaces)

    return normalized_quote

#Function "CheckAnswerFromUser" compares the user answer with the answer from the API. Points are awarded if the answer is correct.
def CheckAnswerFromUser(user_translation):
    global yodaanswerforquote
    if yodaanswerforquote == '':
        return "No quote to translate. Please start a new game with `!mode2`."

    #remove spaces from quotes and standardize apostrophes
    normalized_user_translation = NormalizeQuote(user_translation)
    normalized_api_translation = NormalizeQuote(yodaanswerforquote)

    #check if user translation matches the api translation
    if normalized_user_translation == normalized_api_translation:
        return "correct"
    else:
        return "incorrect"

#Function "ShowSolution" shows the Solution to the User if a quote is loaded.
def ShowSolution():
    global yodaanswerforquote
    if yodaanswerforquote != '':
        global solution_showed
        solution_showed = True
        return yodaanswerforquote
    else:
        return "Error: No solution to show at the moment."