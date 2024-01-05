import requests
#Function "GetYodaQuote": To Get the Yoda Quote from the API    
def GetYodaQuote(SentenceToTranslate):
    #Create API Call
    request_url = "https://api.funtranslations.com/translate/yoda.json?text="
    
    #Create the API Key
    api_key = "P3XfHs2YY0rkfr0KcMt_nQeF"
    headers = {"X-Funtranslations-Api-Secret": api_key}
    #Call the API
    response = requests.get(request_url+SentenceToTranslate, headers=headers)
    
    #Read Out the Translated Sentence if ther is an Answer and Give it Back
    if response.status_code == 200:
        api_data = response.json()
        yoda_text = api_data['contents']['translated']
        yoda_text = ' '.join(yoda_text.split())     
        if yoda_text != '':
            return(yoda_text)
        else:
            return("The text could not be translated or was empty.")
    else:
        print("API Error")