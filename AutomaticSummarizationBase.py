import os
import DbHelper
import DataPreprocessingHelper
import LogHelper
import ExtractiveTextSummarizerBase
import SentenceSimilarityBase
import FileHelper
import DateHelper
import MathHelper
import MajorityTextSummarizer
import AbstractiveTextSummarizerBase
import NamedEntityRecognizerBase
import StemHelper

fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\ThesisBigDatasets\\Multiple Data Summarization\\Multi-Document-Summarization-master\\Multi-Document-Summarization-master\\sample\\fulltext\\"
originalAbstractPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\ThesisBigDatasets\\Multiple Data Summarization\\Multi-Document-Summarization-master\\Multi-Document-Summarization-master\\sample\\summary\\"
#fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\"
#originalAbstractPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\OriginalSummary\\"
generatedAbstractPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Summary\\"
majorityAbstractPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\MajoritySummary\\"
documentTopic = "Sport"
documentSubTopic = "Football"
documentAbstractText = ""
fullTextList = []
abstractTextList = []
mergeFullTextName = "merge.txt"
originalAbstractTextDocumentExtensionType = ".TsSum"
generatedAbstractTextDocumentExtensionType = ".txt"

def StartTextSummarizer():
    DbHelper.TruncateAllTables()
    fullTextList.append(FileHelper.GetDocumentsByGivenPath(fullTextPath))
    iteration = 0
    fullTextDocumentName = ""
    activeAbstractiveTextSummarizationAlgorithms= DbHelper.GetActiveAbstractiveTextSummarizationAlgorithms()
    activeNamedEntityAlgorithmTypes= DbHelper.GetActiveNamedEntityAlgorithmTypes()
    for activeNamedEntityAlgorithmType in activeNamedEntityAlgorithmTypes:
        for activeAbstractiveTextSummarizationAlgorithm in activeAbstractiveTextSummarizationAlgorithms:
            summarizationAlgorithmName = activeAbstractiveTextSummarizationAlgorithm[1]
            summarizationAlgorithmTypeId = activeAbstractiveTextSummarizationAlgorithm[0]
            LogHelper.PrintDebugLog(summarizationAlgorithmName +" algoritması için süreç başladı.")
            iteration = 0
            while(iteration < len(fullTextList[0])):
                startDate=DateHelper.GetCurrentDatetime()
                LogHelper.PrintWarningLog(fullTextList[0][iteration] + " isimli doküman işleme alındı.")
                fullTextDocumentName = fullTextPath + fullTextList[0][iteration] + "\\"  + mergeFullTextName
                originalAbstractFileName = fullTextList[0][iteration].replace("_raw","")
                originalAbstractTextDocumentName = originalAbstractPath + originalAbstractFileName + originalAbstractTextDocumentExtensionType
                fullTextWordsCount = FileHelper.GetCountOfWordsByGivenPath(fullTextDocumentName)
                originalAbstractTextWordsCount = FileHelper.GetCountOfWordsByGivenPath(originalAbstractTextDocumentName)
                summarizationRate = MathHelper.CalculateDivision(originalAbstractTextWordsCount,fullTextWordsCount)
                fullText = FileHelper.GetDocumentContentByGivenPath(fullTextDocumentName)
                fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
                originalDocumentAbstractText = FileHelper.GetDocumentContentByGivenPath(originalAbstractTextDocumentName)
                originalDocumentAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(originalDocumentAbstractText)
                fullTextSentences = FileHelper.GetTextSentencesBySpacy(fullText)
                fullTextSentencesCount = FileHelper.GetCountOfSentences(fullText)
                topSentenceCount = int(MathHelper.CalculateMultiply(summarizationRate,fullTextSentencesCount))
                LogHelper.PrintInfoLog(fullTextList[0][iteration] + " isimli doküman için oluşturulacak özette toplam " + str(topSentenceCount) + " adet cümle olacaktır.")
                documentId = DbHelper.InsertDocument(fullTextDocumentName,fullText,documentTopic,documentSubTopic)
                originalDocumentAbstractId=DbHelper.InsertDocumentAbstracts(documentId,originalDocumentAbstractText)
                namedEntities = SaveWordsAndNamedEntities(documentId,originalDocumentAbstractId,fullTextSentences,True,activeNamedEntityAlgorithmType[0])
                sentencesContainingNamedEntities = FileHelper.GetTextSentencesByContainSearchStatements(fullText,namedEntities)
                generatedAbstractText = FileHelper.GetTextBySentences(sentencesContainingNamedEntities)
                generatedAbstractTextDocumentName = generatedAbstractDirectory + "\\" + originalAbstractFileName
                FileHelper.SaveFile(generatedAbstractTextDocumentName + generatedAbstractTextDocumentExtensionType,generatedAbstractText)
                generatedSummaryId = DbHelper.InsertGeneratedSummaries(documentId,originalDocumentAbstractId,summarizationAlgorithmTypeId,generatedAbstractText)
                LogHelper.PrintInfoLog(fullTextList[0][iteration] + " isimli doküman için özet oluşturuldu.")
                DbHelper.BulkInsertDocumentAbstractSentences(documentId,originalDocumentAbstractId,sentencesContainingNamedEntities)

def SaveWordsAndNamedEntities(documentId,documentAbstractId,sentenceList,isFullTextDocument,namedEntityAlgorithmTypeId):
    allNamedEntities = []
    for sentenceId, sentence in enumerate(sentenceList, start=1):
        if isFullTextDocument ==True:
            DbHelper.InsertSentence(documentId,sentenceId,sentence,sentence)
        else:
            DbHelper.InsertDocumentAbstractSentence(documentId,documentAbstractId,sentenceId,sentence,sentence)
        originalWords=DataPreprocessingHelper.GetCleanedWordsByGivenSentence(sentence)
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Named Entity Recognition süreci başladı.")
        namedEntities = NamedEntityRecognizerBase.FindAndSaveDBNamedEntitiesByGivenAlgorithmType(documentId,documentAbstractId,sentenceId,namedEntityAlgorithmTypeId,isFullTextDocument)
        if len(namedEntities) >0:
            allNamedEntities.append(namedEntities)
        LogHelper.PrintDebugLog(str(sentenceId) +" nolu cümle için Named Entity Recognition süreci bitti.")
        for originalWord in originalWords:
            stemWord=StemHelper.FindStem(originalWord)
            if isFullTextDocument ==True:
                wordId= DbHelper.InsertWord(documentId,sentenceId,stemWord)
                DbHelper.InsertOriginalWord(wordId,originalWord)
            else:
                wordId= DbHelper.InsertDocumentAbstractWords(documentId,documentAbstractId,sentenceId,stemWord)
                DbHelper.InsertDocumentAbstractOriginalWords(wordId,originalWord)
    return allNamedEntities   

StartTextSummarizer()