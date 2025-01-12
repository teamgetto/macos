import LogHelper
import DbHelper
import DataPreprocessingHelper
import FrequencyCalculationHelper
import heapq
import requests
import HtmlDataHelper
import CountryHelper
import DateHelper
import WebSearchBase

excludedTermList = ["yahoo", "google","financeyahoo","yandex","bing","azure"]
countryNameList = CountryHelper.GetCountryNames()
countryNameList = [countryName.lower() for countryName in countryNameList]
htmlTag = "p"
numberOfResultsToReturnInTheResponse = 15
timeout = 5

def FindMeaningFinancialTermsByGivenTerm(financialTerm,topMeaningWordsCount,webSearchId,seedTerm,executedUrlList):
    global page_response
    meaningWordList = []
    LogHelper.PrintDebugLog(financialTerm +" ifadesi için Web arama süreci başlatıldı.")
    activeWebSearchTypes = DbHelper.GetActiveWebSearchTypes()
    for activeWebSearchType in activeWebSearchTypes:
        activeWebSearchTypeId= activeWebSearchType[0]
        urlList = WebSearchBase.Search(financialTerm,numberOfResultsToReturnInTheResponse,timeout,activeWebSearchTypeId)
    for url in urlList:
        if url not in executedUrlList and url is not None:
            try:
                page_response = requests.get(url,timeout=timeout)
                executedUrlList.append(url)
                LogHelper.PrintWarningLog(url)
                DbHelper.InsertVisitedWebSites(webSearchId,url,financialTerm,DateHelper.GetCurrentDatetime())
                break
            except:
                LogHelper.PrintErrorLog(url + "URL alınırken hata oluştu..!")
                pass
        else:
            LogHelper.PrintErrorLog(url + " daha önce işlendi..!")
    documentContent = HtmlDataHelper.GetDocumentContentByGivenParameterHtmlTag(page_response.content,htmlTag)
    if(len(documentContent) != 0):
        documentContent = DataPreprocessingHelper.CleanDocument(documentContent)
        words = DataPreprocessingHelper.GetNonNumericWordListByGivenText(documentContent)
        word_frequencies = FrequencyCalculationHelper.GetWordFrequenciesByWordList(words)
        meaningWordList = heapq.nlargest(topMeaningWordsCount, word_frequencies, key=word_frequencies.get)
        if seedTerm in meaningWordList:
            meaningWordList.remove(seedTerm)
        meaningWordList = set(meaningWordList) - set(excludedTermList)
        meaningWordList = set(meaningWordList) - set(countryNameList)
    return meaningWordList, executedUrlList

#executedUrlList = []
#meaningWordList = []
#seedTerm = "account"
#additionalSearchTerm = ""
#meaningWordList,executedUrlList = FindMeaningFinancialTermsByGivenTerm(seedTerm + " " + additionalSearchTerm,10,1,"finance",executedUrlList)
#print(meaningWordList)
#print(executedUrlList)