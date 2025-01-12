import DbHelper
import LogHelper
import SentenceSimilarityBase
import WordnetHelper
import heapq
import DateHelper
import MeaningWordExtractor
import StemHelper
import NGramHelper

seedSearchTerm = "Voting Democracy Politic"
dictionaryFirstTerm = "Democracy"
dictionaryWordCountThresholdBasedOnSimilarityAlgorithm = 200 
totalDictionaryWords = []
totalSimilarityRates = {}
totalSimilarityRateOfSynonymsWords = {}
executedUrlList = []
thresholdSynonymsWordCount = 10
thresholdMeaningWordCount = 3
thresholdDictionaryWordsCount = 500
topMeaningWordsCount = 10

def Generate():
    webSearchId = DbHelper.InsertWebSearchs(1, DateHelper.GetCurrentDatetime())
    LogHelper.PrintInfoLog(str(webSearchId) + " Web Search Id'li arama başladı.")
    activeSimilarityAlgorithmTypes = DbHelper.GetActiveSimilarityAlgorithmTypes()
    executedUrlList = []
    for activeSimilarityAlgorithmType in activeSimilarityAlgorithmTypes:
        activeSimilarityAlgorithmTypeId = activeSimilarityAlgorithmType[0]
        activeSimilarityAlgorithmName = activeSimilarityAlgorithmType[1]
        LogHelper.PrintInfoLog(activeSimilarityAlgorithmName + " algoritması ile sözlük oluşturulmaya başlanmıştır..!")
        dictionaryWordsBasedOnSimilarityAlgorithm = []
        dictionaryWordsBasedOnSimilarityAlgorithm.append(dictionaryFirstTerm)
        additionalSearchTerm = ""
        while(len(dictionaryWordsBasedOnSimilarityAlgorithm)<dictionaryWordCountThresholdBasedOnSimilarityAlgorithm):
            meaningWordList,executedUrlList = MeaningWordExtractor.FindMeaningFinancialTermsByGivenTerm(seedSearchTerm + " " + additionalSearchTerm,topMeaningWordsCount,webSearchId,dictionaryFirstTerm,executedUrlList)
            totalSimilarityRates = {}
            totalSimilarityRateOfSynonymsWords = {}
            if len(meaningWordList)>0:
                topMeaningWordList = GetThresholdTopMeaningWordList(meaningWordList,dictionaryWordsBasedOnSimilarityAlgorithm,thresholdMeaningWordCount,activeSimilarityAlgorithmTypeId)
                if len(topMeaningWordList)>0 and topMeaningWordList is not None:
                    for topMeaningWord in topMeaningWordList:
                        if topMeaningWord not in dictionaryWordsBasedOnSimilarityAlgorithm:
                            if WordnetHelper.IsWordBelongToEnglishLanguage(topMeaningWord) == True:
                                dictionaryWordsBasedOnSimilarityAlgorithm.append(topMeaningWord)
                            else:
                                LogHelper.PrintErrorLog(topMeaningWord + " kelimesi İngilizce diline ait değildir. Bu nedenle sözlüğe eklenmemiştir..!")
                                topMeaningWordList.remove(topMeaningWord)
                            synonymsWordList = WordnetHelper.FindSynonymsWordsByGivenWord(topMeaningWord)
                            topSynonymsWordList = GetThresholdTopMeaningWordList(synonymsWordList,dictionaryWordsBasedOnSimilarityAlgorithm,thresholdSynonymsWordCount,activeSimilarityAlgorithmTypeId)
                            for topSynonymsWord in topSynonymsWordList:
                                if topSynonymsWord not in dictionaryWordsBasedOnSimilarityAlgorithm:
                                    if WordnetHelper.IsWordBelongToEnglishLanguage(topSynonymsWord) == True:
                                        dictionaryWordsBasedOnSimilarityAlgorithm.append(topSynonymsWord)
                                    else:
                                        LogHelper.PrintErrorLog(topSynonymsWord + " kelimesi İngilizce diline ait değildir. Bu nedenle sözlüğe eklenmemiştir..!")
                                        topSynonymsWordList.remove(topSynonymsWord)
                    additionalSearchTerm = GetAdditionalSearchTerm(topMeaningWordList,topSynonymsWordList)
                    LogHelper.PrintInfoLog(activeSimilarityAlgorithmName + " algoritması kullanılarak sözlük kelime sayısı " + str(len(dictionaryWordsBasedOnSimilarityAlgorithm)) + " değerine ulaştı...")
                else:
                    LogHelper.PrintErrorLog(additionalSearchTerm + " anlamlı kelimesi ile yapılan web arama sürecinde sözlüğe ekleme yapılamamıştır..!")
                    additionalSearchTerm=""
        totalDictionaryWords.append(dictionaryWordsBasedOnSimilarityAlgorithm)
        LogHelper.PrintInfoLog(activeSimilarityAlgorithmName + " algoritması ile sözlük oluşturulmuştur.")
    finalDictionaryWordList = []
    for dictionaryWordsOfSimilarityAlgorithm in totalDictionaryWords:
        for dictionaryWordOfSimilarityAlgorithm in dictionaryWordsOfSimilarityAlgorithm:
            if dictionaryWordOfSimilarityAlgorithm not in finalDictionaryWordList:
                finalDictionaryWordList.append(dictionaryWordOfSimilarityAlgorithm)
    topFinalDictionaryWordList = GetThresholdTopMeaningWordList(finalDictionaryWordList,finalDictionaryWordList,thresholdDictionaryWordsCount,4)
    DbHelper.CompleteWebSearch(webSearchId)
    DbHelper.BulkInsertFinancialTermsDictionary(webSearchId,topFinalDictionaryWordList)
    LogHelper.PrintDebugLog("Sözlüğe eklenecek kelimeler aşağıdaki gibidir.\n")
    for topFinalDictionaryWord in topFinalDictionaryWordList:
        LogHelper.PrintInfoLog(topFinalDictionaryWord)
    LogHelper.PrintInfoLog(str(webSearchId) + " Web Search Id'li arama tamamlandı.")


def GetAdditionalSearchTerm(topMeaningWordList,topSynonymsWordList):
    additionalSearchTerm= ""
    if len(topMeaningWordList)>0 and len(topSynonymsWordList)>0:
        if StemHelper.FindStem(topMeaningWordList[0]) != StemHelper.FindStem(topSynonymsWordList[0]):
            additionalSearchTerm = topMeaningWordList[0] + " " + topSynonymsWordList[0]
        else:
            additionalSearchTerm = topMeaningWordList[0]
    else:
        if len(topMeaningWordList)<=0 and len(topSynonymsWordList)<=0:
            return additionalSearchTerm
        if len(topMeaningWordList)>0 and len(topSynonymsWordList)<=0:
            additionalSearchTerm = topMeaningWordList[0]
        if len(topMeaningWordList)<=0 and len(topSynonymsWordList)>0:
            additionalSearchTerm = topSynonymsWordList[0]
    return additionalSearchTerm


def GetThresholdTopMeaningWordList(list1, list2, thresholdCount,activeSimilarityAlgorithmTypeId):
    totalSimilarityRates = {}
    for word1 in list1:
        totalSimilarityRate = float(0.0)
        for word2 in list2:
            similarityRate = SentenceSimilarityBase.CalculateSimilarity(word1,word2,activeSimilarityAlgorithmTypeId)
            totalSimilarityRate += similarityRate
        totalSimilarityRates[word1] = totalSimilarityRate
    topMeaningWordList = heapq.nlargest(thresholdCount, totalSimilarityRates, key=totalSimilarityRates.get)
    return topMeaningWordList

def EliminateManuelFinancialTermDictionary():
    totalSimilarityRates = {}
    financialTerms = DbHelper.GetFinancialTerms()
    for financialTerm1 in financialTerms:
        totalSimilarityRate = float(0.0)
        for financialTerm2 in financialTerms:
            biGramScore = NGramHelper.CalculateBiGram(financialTerm1,financialTerm2)
            LogHelper.PrintInfoLog(financialTerm1 + " kelimesi ile " + financialTerm2 + " kelimesinin bigram scoru: " + str(biGramScore))
            totalSimilarityRate += biGramScore
        totalSimilarityRates[financialTerm1] = totalSimilarityRate
        LogHelper.PrintWarningLog(financialTerm1 + " kelimesinin toplam bigram scoru: " + str(totalSimilarityRate))
    topFinancialTermList = heapq.nlargest(thresholdDictionaryWordsCount, totalSimilarityRates, key=totalSimilarityRates.get)
    DbHelper.BulkInsertFinancialTermsDictionary(111111,topFinancialTermList)

# Bu metodda manuel finansal terimler sözlüğü ile önerilen otomatik finansal terimler sözlüğünün ortalama benzerlikleri hesaplanmaktadır.
def CalculateAverageSimilarityRate(financialTerms):
    totalSimilarityRate = float(0.0)
    for financialTerm in financialTerms:
        averageSimilarityRateForFinancialTerm = float(0.0)
        for innerFinancialTerm in financialTerms:
            similarityRate = SentenceSimilarityBase.CalculateSimilarity(financialTerm,innerFinancialTerm,7)
            averageSimilarityRateForFinancialTerm += similarityRate
        totalSimilarityRate += averageSimilarityRateForFinancialTerm
    averageSimilarityRate = totalSimilarityRate / len(financialTerms) 
    return averageSimilarityRate

def MergeSentencesAndCalculateAverageSimilarityRate(manuelFinancialTermsDictionary,otomaticFinancialTermsDictionary,activeSimilarityAlgorithmTypeId):
    otomaticFinancialTermsText = ""
    manuelFinancialTermsText = ""
    for otomaticFinancialTerm in otomaticFinancialTermsDictionary:
        otomaticFinancialTermsText += " " + otomaticFinancialTerm[0]
    LogHelper.PrintDebugLog("Otomatik sözlük metni: \n" + otomaticFinancialTermsText)
    LogHelper.PrintWarningLog(otomaticFinancialTermsText)
    for manuelFinancialTerm in manuelFinancialTermsDictionary:
        manuelFinancialTermsText += " " + manuelFinancialTerm
    LogHelper.PrintDebugLog("Manuel sözlük metni: \n" + manuelFinancialTermsText)
    LogHelper.PrintWarningLog(manuelFinancialTermsText)
    similarityRate = SentenceSimilarityBase.CalculateSimilarity(otomaticFinancialTermsText,manuelFinancialTermsText,activeSimilarityAlgorithmTypeId)
    return similarityRate



Generate()
#EliminateManuelFinancialTermDictionary()

#manuelFinancialTermsDictionary = DbHelper.GetFinancialTerms()
#otomaticFinancialTermsDictionary = DbHelper.GetFinancialTermsDictionaryById(10040)
#activeSimilarityAlgorithmTypes = DbHelper.GetActiveSimilarityAlgorithmTypes()
#for activeSimilarityAlgorithmType in activeSimilarityAlgorithmTypes:
#    activeSimilarityAlgorithmTypeId = activeSimilarityAlgorithmType[0]
#    activeSimilarityAlgorithmName = activeSimilarityAlgorithmType[1]
#    averageSimilarityRate = MergeSentencesAndCalculateAverageSimilarityRate(manuelFinancialTermsDictionary,otomaticFinancialTermsDictionary,activeSimilarityAlgorithmTypeId)
#    LogHelper.PrintInfoLog("Otomatik ve manuel sözlüklerinin ortalama " + activeSimilarityAlgorithmName +" metin benzerlik oranı: " + str(averageSimilarityRate))
#averageSimilarityRateForManuelFinancialTermsDictionary = CalculateAverageSimilarityRate(manuelFinancialTermsDictionary)
#averageSimilarityRateForOtomaticFinancialTermsDictionary = CalculateAverageSimilarityRate(otomaticFinancialTermsDictionary)
#LogHelper.PrintInfoLog("Manuel sözlük kelimeleri arasında ortalama metin benzerlik oranı: " + str(averageSimilarityRateForManuelFinancialTermsDictionary))
#LogHelper.PrintInfoLog("Otomatik sözlük kelimeleri arasında ortalama metin benzerlik oranı: " + str(averageSimilarityRateForOtomaticFinancialTermsDictionary))