import requests

subscription_key='806fdf38921049c29a2e0d808a1b202c'
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key" : subscription_key,"mkt":"en-US"}

def Search(search_term,numberOfResultsToReturnInTheResponse,timeout):
    search_term += " language:en"
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML",
               "count":numberOfResultsToReturnInTheResponse,
               "mkt":"en-US"}
    urlList = []
    try:
        response = requests.get(search_url, headers=headers, params=params,timeout=timeout)
        response.raise_for_status()
        for page in response.json()['webPages']['value']:
            page_url = page['url']
            urlList.append(page_url)
        return urlList
    except:
        pass

#result = Search("finance",15,10)
#print(result)