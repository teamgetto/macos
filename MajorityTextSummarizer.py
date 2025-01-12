import FileHelper
import DataPreprocessingHelper
import DbHelper
import MathHelper
import SentenceSimilarityBase
import DateHelper
import LogHelper

def StartMajorityTextSummarizer(generatedAbstractPath,majorityAbstractPath,originalAbstractPath,originalAbstractTextDocumentExtensionType):
    FileHelper.RemoveAllItemsByGivenPath(majorityAbstractPath)
    sentences = []
    activeExtractiveTextSummarizationAlgorithms= DbHelper.GetActiveExtractiveTextSummarizationAlgorithms()
    majorityCount = MathHelper.GetMajorityCountByGivenThreshold(len(activeExtractiveTextSummarizationAlgorithms))
    activeSimilarityAlgorithmTypes= DbHelper.GetActiveSimilarityAlgorithmTypes()
    LogHelper.PrintInfoLog("Majority Count değeri " + str(majorityCount) + " olduğundan, bu değerin altında ortak cümle olması durumunda ilgili cümle özete eklenmeyecektir.")
    for activeExtractiveTextSummarizationAlgorithm in activeExtractiveTextSummarizationAlgorithms:
        generatedAbstractDirectory = generatedAbstractPath + activeExtractiveTextSummarizationAlgorithm[1] + "\\"
        generatedAbstractFileList = FileHelper.GetDocumentsByGivenPath(generatedAbstractDirectory)
        for generatedAbstractFile in generatedAbstractFileList:
            isExistmajorityAbstractFile = FileHelper.CheckPath(majorityAbstractPath + generatedAbstractFile)
            if isExistmajorityAbstractFile == True:
                majorityAbstractText = FileHelper.GetDocumentContentByGivenPath(majorityAbstractPath + generatedAbstractFile)
                sentences = FileHelper.GetTextSentencesBySpacy(majorityAbstractText)
                FileHelper.TruncateFileContent(majorityAbstractPath + generatedAbstractFile)
            else:
                sentences.clear()
            generatedAbstract = FileHelper.GetDocumentContentByGivenPath(generatedAbstractDirectory + generatedAbstractFile)
            generatedAbstract = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(generatedAbstract)
            generatedAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(generatedAbstract)
            for generatedAbstractTextSentence in generatedAbstractTextSentences:
                if generatedAbstractTextSentence not in sentences:
                    numberOfOccurrences = CalculateSentenceExistenceInOtherAbstracts(generatedAbstractFile,generatedAbstractPath,generatedAbstractTextSentence,activeExtractiveTextSummarizationAlgorithms,activeExtractiveTextSummarizationAlgorithm[0])
                    if numberOfOccurrences >= majorityCount: 
                        sentences.append(generatedAbstractTextSentence)
            if len(sentences)>0:
                LogHelper.PrintInfoLog(generatedAbstractFile + " dokümanı için oluşturulan özetlerde ortak " + str(len(sentences)) + " adet cümle bulunmuştur.")
                allSentencesText = ""
                for sentence in sentences:
                    allSentencesText += sentence
                FileHelper.SaveFile(majorityAbstractPath + generatedAbstractFile, allSentencesText)
            else:
                LogHelper.PrintErrorLog(generatedAbstractFile + " dokümanı için oluşturulan özetlerde ortak bir cümle bulunamamıştır.")

    CalculateMajorityTextSummarizationSimilarityRate(activeSimilarityAlgorithmTypes,generatedAbstractPath,majorityAbstractPath,originalAbstractPath,originalAbstractTextDocumentExtensionType)

def CalculateSentenceExistenceInOtherAbstracts(fileName, generatedAbstractPath,sentence,activeExtractiveTextSummarizationAlgorithms,currentSummarizationAlgorithmTypeId):
    numberOfOccurrences = 0
    for activeExtractiveTextSummarizationAlgorithm in activeExtractiveTextSummarizationAlgorithms:
        if currentSummarizationAlgorithmTypeId == activeExtractiveTextSummarizationAlgorithm[0]:
            numberOfOccurrences +=1
        else:
            generatedAbstractFile= generatedAbstractPath + activeExtractiveTextSummarizationAlgorithm[1] + "\\" + fileName
            majorityAbstractText = FileHelper.GetDocumentContentByGivenPath(generatedAbstractFile)
            majorityAbstractText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(majorityAbstractText)
            majorityAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(majorityAbstractText)
            if sentence in majorityAbstractTextSentences:
                numberOfOccurrences +=1
    return numberOfOccurrences


def CalculateMajorityTextSummarizationSimilarityRate(activeSimilarityAlgorithmTypes,generatedAbstractPath,majorityAbstractPath,originalAbstractPath,originalAbstractTextDocumentExtensionType):
    majorityAbstractFileList = FileHelper.GetDocumentsByGivenPath(majorityAbstractPath)
    generalAverageSimilarityRate = float(0.0)
    for majorityAbstractFile in majorityAbstractFileList:
        majorityAbstract = FileHelper.GetDocumentContentByGivenPath(majorityAbstractPath + majorityAbstractFile)
        majorityAbstract = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(majorityAbstract)
        majorityDocumentAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(majorityAbstract)
        originalAbstractFile = FileHelper.RemoveFileExtension(majorityAbstractFile)
        originalAbstractFile = originalAbstractFile + originalAbstractTextDocumentExtensionType
        originalAbstract = FileHelper.GetDocumentContentByGivenPath(originalAbstractPath + originalAbstractFile)
        originalAbstract = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(originalAbstract)
        originalDocumentAbstractTextSentences = FileHelper.GetTextSentencesBySpacy(originalAbstract)
        for activeSimilarityAlgorithmType in activeSimilarityAlgorithmTypes:
            similarityAlgorithmName = activeSimilarityAlgorithmType[1]
            totalSimilarityRate = float(0.0)
            for originalDocumentAbstractTextSentence in originalDocumentAbstractTextSentences:
                for majorityDocumentAbstractTextSentence in majorityDocumentAbstractTextSentences:
                    totalSimilarityRate += SentenceSimilarityBase.CalculateSimilarity(originalDocumentAbstractTextSentence,majorityDocumentAbstractTextSentence,activeSimilarityAlgorithmType[0])
            totalSentence = MathHelper.CalculateMultiply(len(majorityDocumentAbstractTextSentences),len(originalDocumentAbstractTextSentences))
            averageSimilarityRate = MathHelper.CalculateDivision(totalSimilarityRate,totalSentence)
            generalAverageSimilarityRate += averageSimilarityRate
            LogHelper.PrintInfoLog(majorityAbstractFile + " isimli doküman için majority özet ile orijinal özet arasındaki ortalama benzerlik oranı " + similarityAlgorithmName + " benzerlik algoritması ile " + str(averageSimilarityRate)+ " olarak tespit edildi.")
    generalResult = MathHelper.CalculateDivision(generalAverageSimilarityRate,len(majorityAbstractFileList))
    LogHelper.PrintInfoLog("Tüm genelde başarım oranı: " + str(generalResult))