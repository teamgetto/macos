import os
import datetime
import DbHelper
import DataPreprocessingHelper
import StemHelper
import LogHelper
import HtmlDataHelper
import FileHelper
import SpellCheckerBase
import NamedEntityRecognizerBase
import UserPreferenceHelper
import ExtractiveTextSummarizerBase

fullTextPathForDocumentAndSummaryInTheSameFile= "C:\\Users\\TFKB\\Desktop\\Papers\\PHD\\Thesis\\Datasets\\Xml\\"
fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\"
abstractPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Summary\\"
documentTopic = "Sport"
documentSubTopic = "Football"
documentAbstractText = ""
fullTextList = []
abstractTextList = []
summarizationAlgorithmType = 1 # 1:Extractive and 2: Abstractive
topSentenceCount = 4

def StartBasicDocumentVerification():
    DbHelper.TruncateAllTables()
    mainDocumentAndSummaryInTheSameFile = False
    #mainDocumentAndSummaryInTheSameFile = UserPreferenceHelper.GetUserPreference()
    GetFullTextList(mainDocumentAndSummaryInTheSameFile)
    
    LogHelper.PrintInfoLog("Extractive özetleme süreci başladı.")
    ExtractiveTextSummarizerBase.GenerateSummaries(fullTextPath,abstractPath,topSentenceCount)
    LogHelper.PrintInfoLog("Extractive özetleme süreci bitti.")
    iteration = 0
    fullTextDocumentName = ""
    activeNamedEntityAlgorithmTypes= DbHelper.GetActiveNamedEntityAlgorithmTypes()
    activeSpellCheckerAlgorithmTypes= DbHelper.GetActiveSpellCheckerAlgorithmTypes()
    activeExtractiveTextSummarizationAlgorithms= DbHelper.GetActiveExtractiveTextSummarizationAlgorithms()
    for namedEntityAlgorithmTypeId in activeNamedEntityAlgorithmTypes:
        for spellCheckerAlgorithmTypeId in activeSpellCheckerAlgorithmTypes:
            for activeExtractiveTextSummarizationAlgorithm in activeExtractiveTextSummarizationAlgorithms:
                summarizationAlgorithmName = activeExtractiveTextSummarizationAlgorithm[1]
                summarizationAlgorithmTypeId = activeExtractiveTextSummarizationAlgorithm[0]
                iteration = 0
                while(iteration < len(fullTextList[0])):
                    startDate=datetime.datetime.now()
                    LogHelper.PrintInfoLog(str(iteration)+". sıradaki " + fullTextList[0][iteration] + " isimli doküman okunmaya başlandı.")
                    if mainDocumentAndSummaryInTheSameFile == True:
                        fullTextDocumentName =fullTextPathForDocumentAndSummaryInTheSameFile + fullTextList[0][iteration]
                        originalText = FileHelper.GetDocumentContentByGivenPath(fullTextDocumentName)
                        fullText = HtmlDataHelper.GetDocumentContentWithSpecifiedParentTag(originalText,"p","div")
                        documentAbstractText = HtmlDataHelper.GetDocumentContentWithSpecifiedParentTag(originalText,"p","abstract")
                        fullText=HtmlDataHelper.RemoveHtmlTags(fullText)
                    else:
                        fullTextDocumentName =fullTextPath + fullTextList[0][iteration]
                        abstractTextDocumentName =abstractPath + summarizationAlgorithmName + "\\" + fullTextList[0][iteration]
                        fullText = FileHelper.GetDocumentContentByGivenPath(fullTextDocumentName)
                        documentAbstractText = FileHelper.GetDocumentContentByGivenPath(abstractTextDocumentName)

                    fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
                    documentAbstractText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(documentAbstractText)
                    documentId = DbHelper.InsertDocument(fullTextDocumentName,fullText,documentTopic,documentSubTopic)
                    documentAbstractId=DbHelper.InsertDocumentAbstracts(documentId,documentAbstractText)
                    fullTextSentences = FileHelper.GetTextSentencesBySpacy(fullText)
                    LogHelper.PrintDebugLog("Ana doküman toplam cümle sayısı: " + str(len(fullTextSentences)))
                    SaveWordsAndNamedEntities(documentId,documentAbstractId,fullTextSentences,True,spellCheckerAlgorithmTypeId[0],namedEntityAlgorithmTypeId[0])
                    documentAbstractSentences = FileHelper.GetTextSentencesBySpacy(documentAbstractText)

                    LogHelper.PrintDebugLog("Özet doküman toplam cümle sayısı: " + str(len(documentAbstractSentences)))
                    SaveWordsAndNamedEntities(documentId,documentAbstractId,documentAbstractSentences,False,spellCheckerAlgorithmTypeId[0],namedEntityAlgorithmTypeId[0])

                    documentNamedEntities = DbHelper.GetDistinctDocumentNamedEntities(documentId)
                    documentNamedEntities = DataPreprocessingHelper.RemoveStripByGivenItemList(documentNamedEntities)
                    abstractTextNamedEntities = DbHelper.GetDistinctDocumentAbstractNamedEntities(documentId,documentAbstractId)
                    abstractTextNamedEntities = DataPreprocessingHelper.RemoveStripByGivenItemList(abstractTextNamedEntities)
                    totalNumberOfNamedEntities = len(abstractTextNamedEntities)
                    numberOfNamedEntitiesMatched =0
                    for abstractTextNamedEntity in abstractTextNamedEntities:
                        for documentNamedEntity in documentNamedEntities:
                            if abstractTextNamedEntity == documentNamedEntity:
                                numberOfNamedEntitiesMatched +=1
                                LogHelper.PrintInfoLog("Özet dokümanda bulunan " + abstractTextNamedEntity + " Named Entity kelimesi ana dokümanda da bulunmaktadır.")
                                break
                    LogHelper.PrintInfoLog("Eşleşen Named Entity Sayısı: " + str(numberOfNamedEntitiesMatched))
                    LogHelper.PrintInfoLog("Özette tespit edilen Named Entity sayısı: " + str(totalNumberOfNamedEntities))
                    successRate = (numberOfNamedEntitiesMatched/totalNumberOfNamedEntities) *100
                    endDate=datetime.datetime.now()
                    DbHelper.InsertPerformanceEvaluationResults(documentId,documentAbstractId,successRate,numberOfNamedEntitiesMatched,totalNumberOfNamedEntities,namedEntityAlgorithmTypeId[0],spellCheckerAlgorithmTypeId[0],summarizationAlgorithmType,summarizationAlgorithmTypeId,datetime.datetime.now(),str(endDate-startDate))
                    LogHelper.PrintInfoLog("Doküman Id: " + str(documentId) + " ve Doküman Özet Id: " + str(documentAbstractId) +" için Başarım Oranı % " + str(successRate))
                    iteration+=1

def GetFullTextList(mainDocumentAndSummaryInTheSameFile):
    if mainDocumentAndSummaryInTheSameFile == True:
        fullTextList.append(sorted(os.listdir(fullTextPathForDocumentAndSummaryInTheSameFile)))
        if len(fullTextList[0])== 0:
            LogHelper.PrintErrorLog(fullTextPathForDocumentAndSummaryInTheSameFile+ " adresinde doküman bulunmamaktadır.")
        else :
            LogHelper.PrintInfoLog(fullTextPathForDocumentAndSummaryInTheSameFile +" adresinde toplam "+ str(len(fullTextList[0]))+ " adet doküman bulunmaktadır.")
    else:
        fullTextList.append((os.listdir(fullTextPath)))
        if len(fullTextList[0])== 0:
            LogHelper.PrintErrorLog(fullTextPath+ " adresinde doküman bulunmamaktadır.")
        else :
            LogHelper.PrintInfoLog(fullTextPath +" adresinde toplam "+ str(len(fullTextList[0]))+ " adet doküman bulunmaktadır.")
        abstractTextList.append((os.listdir(abstractPath)))
        if len(abstractTextList[0])==0:
            LogHelper.PrintErrorLog(abstractPath+ " adresinde doküman bulunmamaktadır.")
        else :
            LogHelper.PrintInfoLog(abstractPath +" adresinde toplam "+ str(len(abstractTextList[0]))+ " adet özet doküman bulunmaktadır.")

def SaveWordsAndNamedEntities(documentId,documentAbstractId,sentenceList,isFullTextDocument,spellCheckerAlgorithmTypeId,namedEntityAlgorithmTypeId):
    for sentenceId, sentence in enumerate(sentenceList, start=1):
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Spell Checker süreci başladı.")
        sentenceAfterSpell = SpellCheckerBase.SpellCheckByGivenAlgorithmType(spellCheckerAlgorithmTypeId,sentence)
        if len(sentenceAfterSpell)==0:
            sentenceAfterSpell=sentence
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Spell Checker süreci bitti.")
        if isFullTextDocument ==True:
            DbHelper.InsertSentence(documentId,sentenceId,sentenceAfterSpell,sentence)
        else:
            DbHelper.InsertDocumentAbstractSentence(documentId,documentAbstractId,sentenceId,sentenceAfterSpell,sentence)
        originalWords=DataPreprocessingHelper.GetCleanedWordsByGivenSentence(sentenceAfterSpell)
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Named Entity Recognition süreci başladı.")
        namedEntities = NamedEntityRecognizerBase.FindAndSaveDBNamedEntitiesByGivenAlgorithmType(documentId,documentAbstractId,sentenceId,namedEntityAlgorithmTypeId,isFullTextDocument)
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Named Entity Recognition süreci bitti.")
        for originalWord in originalWords:
            stemWord=StemHelper.FindStem(originalWord)
            if isFullTextDocument ==True:
                wordId= DbHelper.InsertWord(documentId,sentenceId,stemWord)
                DbHelper.InsertOriginalWord(wordId,originalWord)
            else:
                wordId= DbHelper.InsertDocumentAbstractWords(documentId,documentAbstractId,sentenceId,stemWord)
                DbHelper.InsertDocumentAbstractOriginalWords(wordId,originalWord)