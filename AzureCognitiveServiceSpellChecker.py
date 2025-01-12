import requests
import json

key = "b35da065165140c6b6e79ebd3bf129e2"
endpoint = 'https://api.cognitive.microsoft.com/bing/v7.0/spellcheck'

def SpellChecker(sentence):
    data = {'text': sentence}
    params = {
        'mkt':'en-us',
        'mode':'proof'
        }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': key,
        }
    response = requests.post(endpoint, headers=headers, params=params, data=data)
    jsonResponse = json.dumps(response.json(), indent=2)
    dictResponse = json.loads(jsonResponse)
    flaggedTokens = dictResponse['flaggedTokens']
    corrected = ''
    i = 0
    for flagged in flaggedTokens:
        offset = flagged['offset']
        token = flagged['token']
        suggestion = flagged['suggestions'][0]['suggestion']
        corrected = corrected + sentence[i:offset] + suggestion
        i = offset + len(token)
    corrected = corrected + sentence[i:len(sentence)]
    return corrected

#Usage -->
#sentence = "Footbal and basebal hav been lockd in a perpetal battle for the afection of sports in the United States."
#print("Sentence before spellchecker  --> " + sentence)
#print("Sentence after spellchecker  --> " + SpellChecker(sentence))