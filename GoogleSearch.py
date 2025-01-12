import LogHelper

#url = "https://console.developers.google.com/apis/credentials/key/18780e84-a7c9-420b-8b29-74b1f13dce82?authuser=0&project=phdthesisdocumentverification"
apiKey = "AIzaSyAFJywUkWPMWBpTIfAe_TZkbYXQPUvdkKE"
cse_id = "017576662512468239146:omuauf_lfve"

def Search(searchTerm, numberOfResultsToReturnInTheResponse,timeout):
    service = build("customsearch", "v1", developerKey=apiKey)
    resultItems = service.cse().list(q=searchTerm, cx=cse_id,lr="lang_en",num=numberOfResultsToReturnInTheResponse,hl="en").execute().get('items', [])
    urlList = []
    for page in resultItems:
        page_url = page['link']
        try:
           urlList.append(page_url)
           return urlList
        except Exception as exception:
            LogHelper.PrintErrorLog("Google Search İşleminde Hata Oluştu: Hata: " + str(exception))