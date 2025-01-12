import FileHelper
import FrequencyCalculationHelper
import DataPreprocessingHelper
from math import factorial
import heapq
import math
import nltk
import MathHelper

def GenerateSummary(text,topSentenceCount):
    sentences = FileHelper.GetTextSentencesBySpacy(text)
    wordFrequencies = FrequencyCalculationHelper.GetWordFrequenciesByGivenText(text)
    wordList = DataPreprocessingHelper.GetWordListByGivenText(text)
    D = len(wordList)
    meaningValues = {}
    for word in wordList:
        if word in wordFrequencies.keys():
            m= getM(sentences,word)
            K = wordFrequencies[word]
            P=GetP(sentences,word)
            N=GetN(D,P)
            if K==0 or m==0:
                    K+=1
                    m+=1
            combinationValue=CalculateCombinations(K,m)
            numberOfFalseAlarms= combinationValue * (1/(float(N)**(m-1)))
            meaningValue= float(numberOfFalseAlarms) / m
            #meaningValue = MathHelper.CalculateLog(float(numberOfFalseAlarms)) /-m
            meaningValues[word] = meaningValue
    sentenceScores = CalculateSentenceScores(sentences,meaningValues)
    summarySentences = heapq.nlargest(topSentenceCount, sentenceScores, key=sentenceScores.get)
    summary = ' '.join(summarySentences)
    return summary

def GetP(sentences,word):
    count = 0
    for sentence in sentences:
        if word in sentence:
            sentenceWordCount = FileHelper.GetCountOfWordsByGivenText(sentence)
            count +=sentenceWordCount
    return count    

def GetN(D,P):
    if P == 0:
        P=1
    return D/P

def CalculateCombinations(n, r):
    if n-r < 0:
        return 1
    return MathHelper.CalculateFactorial(n) // MathHelper.CalculateFactorial(r) // MathHelper.CalculateFactorial(n-r)

def getM(sentences,word):
    count = 0
    for sentence in sentences:
        if word in sentence:
            count +=1
    return count

def CalculateSentenceScores(sentences,meaningValues):
    sentenceScores = {}
    for sentence in sentences:
        sentence = sentence
        for word in nltk.word_tokenize(sentence):
            if word in meaningValues.keys():
                if sentence not in sentenceScores.keys():
                    sentenceScores[sentence] = meaningValues[word]
                else:
                    sentenceScores[sentence] += meaningValues[word]

    return sentenceScores

#Usage -->
#topSentenceCount = 5
#fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\001.txt"
#fullText = FileHelper.GetDocumentContentByGivenPath(fullTextPath)
#fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
#print("Full Text: \n" +fullText)
#summaryText = GenerateSummary(fullText,topSentenceCount)
#print("Summary Text: \n" + summaryText)