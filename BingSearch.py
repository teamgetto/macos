
def Search(search_term,numberOfResultsToReturnInTheResponse,timeout):
    search_term += " language:en"
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML",
               "mkt":"en-US"}
    try:
      response = requests.get(bing_search_url, headers=headers, params=params,timeout=timeout)
      response.raise_for_status()
      for page in response.json()['webPages']['value']:
        page_url = page['url']
        SaveDocumentGivenURL(page_url)
    except:
       pass

