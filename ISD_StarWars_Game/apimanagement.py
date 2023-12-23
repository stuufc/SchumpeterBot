import requests
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