from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import DataPreprocessingHelper
import LogHelper

def CalculateSimilarity(mainSentence, searchSentence):
    cosineSimilarity = float(0.5)
    try:
        mainSentenceWordList = DataPreprocessingHelper.GetCleanedWordsByGivenSentence(mainSentence)
        searchSentenceWordList = DataPreprocessingHelper.GetCleanedWordsByGivenSentence(searchSentence)
        combinedWordList = mainSentenceWordList + searchSentenceWordList
        l1 =[];l2 =[]
        for word in combinedWordList:
             if word in mainSentenceWordList:
                 l1.append(1)
             else:
                 l1.append(0)
         
             if word in searchSentenceWordList:
                 l2.append(1)
             else:
                 l2.append(0)

        c = 0
        for i in range(len(combinedWordList)):
            c+= l1[i]*l2[i]

        cosineSimilarity = c / float((sum(l1)*sum(l2))**0.5)
        return cosineSimilarity

    except Exception as err:
        LogHelper.PrintErrorLog("Encountered exception in Cosine Similarity {}".format(err))
        return cosineSimilarity

        

# Usage -->
#mainSentence ="I love horror movies"
#searchSentence ="Lights out is a horror movie"
#result = CalculateSimilarity(mainSentence,searchSentence)
#print(result)