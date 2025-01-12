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
    activeExtractiveTextSummarizationAlgorithms= DbHelper.GetActiveExtractiveTextSummarizationAlgorithms()
    activeSimilarityAlgorithmTypes= DbHelper.GetActiveSimilarityAlgorithmTypes()
    for activeExtractiveTextSummarizationAlgorithm in activeExtractiveTextSummarizationAlgorithms:
        summarizationAlgorithmName = activeExtractiveTextSummarizationAlgorithm[1]
        summarizationAlgorithmTypeId = activeExtractiveTextSummarizationAlgorithm[0]
        LogHelper.PrintDebugLog(summarizationAlgorithmName +" algoritması için süreç başladı.")
        generatedAbstractDirectory = generatedAbstractPath + activeExtractiveTextSummarizationAlgorithm[1]
        isExist = FileHelper.CheckPath(generatedAbstractDirectory)
        if isExist == False:
            FileHelper.CreateDirectory(generatedAbstractDirectory)
            LogHelper.PrintErrorLog(generatedAbstractDirectory + " klasörü bulunmadığı için oluşturuldu.")
        removalPath = generatedAbstractPath + activeExtractiveTextSummarizationAlgorithm[1] + "\\"
        FileHelper.RemoveAllItemsByGivenPath(removalPath)
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
            DbHelper.BulkInsertDocumentSentences(documentId,fullTextSentences)
            generatedAbstractText = ExtractiveTextSummarizerBase.SummarizeDocumentByGivenAlgorithmType(fullText,activeExtractiveTextSummarizationAlgorithm[0],topSentenceCount)
            generatedAbstractTextDocumentName = generatedAbstractDirectory + "\\" + originalAbstractFileName
            FileHelper.SaveFile(generatedAbstractTextDocumentName + generatedAbstractTextDocumentExtensionType,generatedAbstractText)
            generatedSummaryId = DbHelper.InsertGeneratedSummaries(documentId,originalDocumentAbstractId,summarizationAlgorithmTypeId,generatedAbstractText)
            LogHelper.PrintInfoLog(fullTextList[0][iteration] + " isimli doküman için özet oluşturuldu.")
            generatedAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(generatedAbstractText)
            DbHelper.BulkInsertDocumentAbstractSentences(documentId,originalDocumentAbstractId,generatedAbstractTextSentences)
            for activeSimilarityAlgorithmType in activeSimilarityAlgorithmTypes:
                similarityAlgorithmName = activeSimilarityAlgorithmType[1]
                totalSimilarityRate = float(0.0)
                for originalDocumentAbstractTextSentence in originalDocumentAbstractTextSentences:
                    for generatedAbstractTextSentence in generatedAbstractTextSentences:
                        similarityRate = SentenceSimilarityBase.CalculateSimilarity(originalDocumentAbstractTextSentence,generatedAbstractTextSentence,activeSimilarityAlgorithmType[0])
                        totalSimilarityRate += similarityRate
                        LogHelper.PrintInfoLog(generatedAbstractTextSentence + "\n oluşturulan özetin cümlesi ile " + originalDocumentAbstractTextSentence + "\n mevcut özetin cümlesinin benzerlik oranı " + str(similarityRate) + " olarak tespit edildi.")
                endDate=DateHelper.GetCurrentDatetime()
                LogHelper.PrintInfoLog(originalAbstractFileName + " isimli doküman için toplam benzerlik oranı: " + str(totalSimilarityRate))
                totalSentence = MathHelper.CalculateMultiply(len(generatedAbstractTextSentences),len(originalDocumentAbstractTextSentences))
                LogHelper.PrintInfoLog(originalAbstractFileName + " isimli doküman için toplam bölüm değeri: " + str(totalSentence))
                averageSimilarityRate = MathHelper.CalculateDivision(totalSimilarityRate, totalSentence)
                DbHelper.InsertSimilarityRateResults(documentId,originalDocumentAbstractId,generatedSummaryId,activeSimilarityAlgorithmType[0],averageSimilarityRate,DateHelper.GetCurrentDatetime(), DateHelper.GetDifferenceDate(endDate,startDate))
                LogHelper.PrintInfoLog(originalAbstractFileName + " isimli doküman için " + summarizationAlgorithmName  +" özetleme algoritması ile oluşturulan özet ile orijinal özet arasındaki ortalama benzerlik oranı " + similarityAlgorithmName + " benzerlik algoritması ile " + str(averageSimilarityRate)+ " olarak tespit edildi.")
            LogHelper.PrintInfoLog(originalAbstractFileName + " isimli doküman için süreç tamamlandı.")
            iteration+=1
        LogHelper.PrintInfoLog(summarizationAlgorithmName +" algoritması için süreç tamamlandı.")
    LogHelper.PrintInfoLog("Uygulama başarıyla işlemleri tamamladı.")
    MajorityTextSummarizer.StartMajorityTextSummarizer(generatedAbstractPath,majorityAbstractPath,originalAbstractPath,originalAbstractTextDocumentExtensionType)
            
#StartTextSummarizer()