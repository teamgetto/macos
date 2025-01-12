import pypyodbc
import FileHelper
import random
import DateHelper

def GetDocumentWords():
    SQLCommand = ("select * from DocumentVerification.dbo.Words w(nolock)")
    cursor.execute(SQLCommand)
    words = cursor.fetchall()
    return words

def DeleteAllWords():
    SQLCommand = ("delete from DocumentVerification.dbo.Words")
    cursor.execute(SQLCommand)
    connection.commit() 
    
def GetWordsCountByDocumentId(documentId):
    cursor.execute("SELECT count(*) FROM [DocumentVerification].[dbo].[Words] (nolock) where DocumentId=?",[documentId])
    result_set = cursor.fetchall()
    number_of_rows_Words = result_set[0][0]
    return number_of_rows_Words

def GetDocumentAbstractOriginalWords(documentId, documentAbstractId):
    SQLCommand = ("select daow.OriginalWord from DocumentVerification.dbo.DocumentAbstractOriginalWords daow(nolock) inner join DocumentVerification.dbo.DocumentAbstractWords daw(nolock) on daow.WordId=daw.WordId  where daw.DocumentId=? and daw.DocumentAbstractId = ?")
    Values = [documentId,documentAbstractId]
    cursor.execute(SQLCommand,Values)
    documentAbstractOriginalWords = cursor.fetchall()
    return documentAbstractOriginalWords

def GetLastIdByGivenTable(tableName,columnName):
    SQLCommand = ("select Max(" +columnName + ") from DocumentVerification.dbo." + tableName+ " (nolock)")
    cursor.execute(SQLCommand)
    result = cursor.fetchall()
    if result[0][0] is None:
        return 0
    else:
        return result[0][0]

def GetDocumentNamedEntities(documentId):
    SQLCommand = ("select EntityText from DocumentVerification.dbo.NamedEntities (nolock) where DocumentId=?")
    Values = [documentId]
    cursor.execute(SQLCommand,Values)
    documentNamedEntities = cursor.fetchall()
    return documentNamedEntities

def GetDistinctDocumentNamedEntities(documentId):
    SQLCommand = ("select Distinct(EntityText) from DocumentVerification.dbo.NamedEntities (nolock) where DocumentId=?")
    Values = [documentId]
    cursor.execute(SQLCommand,Values)
    documentNamedEntities = cursor.fetchall()
    return documentNamedEntities

def GetDistinctDocumentSentenceNamedEntities(documentId,sentenceId):
    SQLCommand = ("select Distinct(EntityText) from DocumentVerification.dbo.NamedEntities (nolock) where DocumentId=? and SentenceId=?")
    Values = [documentId,sentenceId]
    cursor.execute(SQLCommand,Values)
    documentSentenceNamedEntityList = cursor.fetchall()
    return documentSentenceNamedEntityList

def GetDistinctDocumentAbstractNamedEntities(documentId,documentAbstractId):
    SQLCommand = ("select Distinct(EntityText) from DocumentVerification.dbo.DocumentAbstractNamedEntities (nolock) where DocumentId=? and DocumentAbstractId =?")
    Values = [documentId,documentAbstractId]
    cursor.execute(SQLCommand,Values)
    documentNamedEntities = cursor.fetchall()
    return documentNamedEntities

def GetDistinctDocumentAbstractSentenceNamedEntities(documentId,documentAbstractId,documentAbstractSentenceId):
    SQLCommand = ("select Distinct(EntityText) from DocumentVerification.dbo.DocumentAbstractNamedEntities (nolock) where DocumentId=? and DocumentAbstractId =? and DocumentAbstractSentenceId=?")
    Values = [documentId,documentAbstractId,documentAbstractSentenceId]
    cursor.execute(SQLCommand,Values)
    documentAbstractSentenceNamedEntityList = cursor.fetchall()
    return documentAbstractSentenceNamedEntityList

def GetActiveSpellCheckerAlgorithmTypes():
    SQLCommand = ("select SpellCheckerAlgorithmTypeId from DocumentVerification.dbo.SpellCheckerAlgorithmTypes (nolock) where IsActive =1")
    cursor.execute(SQLCommand)
    activeSpellCheckerAlgorithmTypes = cursor.fetchall()
    return activeSpellCheckerAlgorithmTypes

def GetActiveNamedEntityAlgorithmTypes():
    SQLCommand = ("select NamedEntityAlgorithmTypeId from DocumentVerification.dbo.NamedEntityAlgorithmTypes (nolock) where IsActive =1")
    cursor.execute(SQLCommand)
    activeNamedEntityAlgorithmTypes = cursor.fetchall()
    return activeNamedEntityAlgorithmTypes

def GetActiveExtractiveTextSummarizationAlgorithms():
    SQLCommand = ("select ExtractiveTextSummarizationAlgorithmTypeId, ExtractiveTextSummarizationAlgorithmName from DocumentVerification.dbo.ExtractiveTextSummarizationAlgorithmTypes (nolock) where IsActive =1")
    cursor.execute(SQLCommand)
    activeExtractiveTextSummarizationAlgorithmTypes = cursor.fetchall()
    return activeExtractiveTextSummarizationAlgorithmTypes

def GetActiveAbstractiveTextSummarizationAlgorithms():
    SQLCommand = ("select AbstractiveTextSummarizationAlgorithmTypeId, AbstractiveTextSummarizationAlgorithmName from DocumentVerification.dbo.AbstractiveTextSummarizationAlgorithmTypes (nolock) where IsActive =1")
    cursor.execute(SQLCommand)
    activeAbstractiveTextSummarizationAlgorithmTypes = cursor.fetchall()
    return activeAbstractiveTextSummarizationAlgorithmTypes

def GetActiveSimilarityAlgorithmTypes():
    SQLCommand = ("select SimilarityAlgorithmTypeId, SimilarityAlgorithmName from DocumentVerification.dbo.SimilarityAlgorithmTypes (nolock) where IsActive = 1")
    cursor.execute(SQLCommand)
    activeSimilarityAlgorithmTypes = cursor.fetchall()
    return activeSimilarityAlgorithmTypes

def GetBestSimilarSentences(topCount, abstractSentenceId, similarityAlgorithmTypeId):
    SQLCommand = ("select TOP (?) s.SentenceId from DocumentVerification.dbo.SentenceSimilarityResults ssr(nolock) inner join DocumentVerification.dbo.Sentences s(nolock) on s.SentenceId = ssr.OriginalSentenceId where AbstractSentenceId = ? and SimilarityAlgorithmTypeId = ? order by ssr.SimilarityRate desc")
    Values = [topCount,abstractSentenceId,similarityAlgorithmTypeId]
    cursor.execute(SQLCommand,Values)
    bestSimilarSentenceIdList= cursor.fetchall()
    return bestSimilarSentenceIdList

def GetSimilarSentences(topCount, abstractSentenceId, similarityAlgorithmTypeId):
    similarSentenceIdList = []
    SQLCommand = ("select TOP (?) ssr.OriginalSentenceId from DocumentVerification.dbo.SentenceSimilarityResults ssr(nolock) where ssr.AbstractSentenceId = ? and ssr.SimilarityAlgorithmTypeId = ? order by ssr.SimilarityRate desc")
    Values = [topCount,abstractSentenceId,similarityAlgorithmTypeId]
    cursor.execute(SQLCommand,Values)
    innerSimilarSentenceIdList= cursor.fetchall()
    for similarSentenceId in innerSimilarSentenceIdList:
        similarSentenceIdList.append(similarSentenceId[0])
    return similarSentenceIdList

def GetDocumentSentenceList(documentId):
    SQLCommand = ("select s.SentenceText, s.SentenceId from DocumentVerification.dbo.Sentences s(nolock) where s.DocumentId IN (?)")
    Values = [documentId]
    cursor.execute(SQLCommand,Values)
    sentenceList= cursor.fetchall()
    return sentenceList


def GetSentenceListById(sentenceIdList):
    bestSimilarSentenceList = []
    SQLCommand = ("select s.SentenceText from DocumentVerification.dbo.Sentences s(nolock) where s.SentenceId IN {};").format(sentenceIdList)
    cursor.execute(SQLCommand)
    sentenceList= cursor.fetchall()
    for sentence in sentenceList:
        bestSimilarSentenceList.append(sentence[0])
    return bestSimilarSentenceList

def GetOriginalDocumentSentenceTextById(documentId, sentenceId):
    SQLCommand = ("select s.SentenceText from DocumentVerification.dbo.Sentences s(nolock) where s.DocumentId = ? and s.SentenceId = ?")
    Values = [documentId, sentenceId]
    cursor.execute(SQLCommand,Values)
    sentenceText = cursor.fetchall()
    return sentenceText[0][0]

def GetAbstractDocumentSentenceTextById(documentId, documentAbstractId, documentAbstractSentenceId):
    SQLCommand = ("select das.DocumentAbstractSentenceText from DocumentVerification.dbo.DocumentAbstractSentences das(nolock) where das.DocumentId = ? and das.DocumentAbstractId = ? and das.DocumentAbstractSentenceId = ?")
    Values = [documentId, documentAbstractId, documentAbstractSentenceId]
    cursor.execute(SQLCommand,Values)
    documentAbstractSentenceText = cursor.fetchall()
    return documentAbstractSentenceText[0][0]

def GetFinancialTerms():
    financialTermList = []
    SQLCommand = ("select top 50 f.FinancialTerm from DocumentVerification.dbo.FinancialTerms f(nolock) where f.IsActive=1")
    cursor.execute(SQLCommand)
    termList= cursor.fetchall()
    for term in termList:
        financialTermList.append(term[0])
    financialTermList = [financialTerm.lower() for financialTerm in financialTermList]
    return financialTermList

def GetActiveWebSearchTypes():
    SQLCommand = ("select WebSearchTypeId, WebSearchName from DocumentVerification.dbo.WebSearchTypes (nolock) where IsActive =1")
    cursor.execute(SQLCommand)
    activeWebSearchTypes = cursor.fetchall()
    return activeWebSearchTypes

def GetFinancialTermsDictionaryById(webSearchId):
    financialTermList = []
    SQLCommand = ("select top 50 FinancialTerm from DocumentVerification.dbo.FinancialTermsDictionary (nolock) where WebSearchId =?")
    Values = [webSearchId]
    cursor.execute(SQLCommand,Values)
    financialTerms= cursor.fetchall()
    for financialTerm in financialTerms:
        financialTermList.append(financialTerm[0])
    financialTermList = [financialTerm.lower() for financialTerm in financialTermList]
    return financialTermList

def CompleteWebSearch(webSearchId):
    SQLCommand = ("Update DocumentVerification.dbo.WebSearchs set IsActive = 0 where WebSearchId= ?")
    Values = [webSearchId]
    cursor.execute(SQLCommand,Values)
    connection.commit()

def InsertOriginalWord(wordId,originalWord):
    SQLCommand = ("INSERT INTO OriginalWords (WordId,OriginalWord)  VALUES (?,?)")
    Values = [wordId,originalWord]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertWord(documentId,sentenceId,word):
    SQLCommand = ("INSERT INTO Words (DocumentId, SentenceId, Word)  VALUES (?,?,?)")
    Values = [documentId,sentenceId,word]
    cursor.execute(SQLCommand,Values)
    wordId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return wordId

def InsertDocument(documentName,documentText,documentTopic,documentSubTopic):
    SQLCommand = ("INSERT INTO Documents (DocumentName,DocumentText,DocumentTopic,DocumentSubTopic)  VALUES (?,?,?,?)")
    Values = [documentName,documentText,documentTopic,documentSubTopic]
    cursor.execute(SQLCommand,Values)
    documentId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return documentId

def InsertSentence(documentId,sentenceId,sentenceText,sentenceTextBeforeSpellChecking):
    SQLCommand = ("INSERT INTO Sentences (DocumentId,SentenceId,SentenceText,SentenceTextBeforeSpellChecking)  VALUES (?,?,?,?)")
    Values = [documentId,sentenceId,sentenceText,sentenceTextBeforeSpellChecking]
    cursor.execute(SQLCommand,Values)
    connection.commit()

def InsertNamedEntity(documentId, sentenceId, entityText, entityCategory, entitySubCategory):
    SQLCommand = ("INSERT INTO NamedEntities (DocumentId, SentenceId, EntityText, EntityCategory, EntitySubCategory)  VALUES (?,?,?,?,?)")
    Values = [documentId, sentenceId, entityText, entityCategory, entitySubCategory]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertDocumentAbstracts(documentId,documentAbstractText):
    SQLCommand = ("INSERT INTO DocumentAbstracts (DocumentId,DocumentAbstractText)  VALUES (?,?)")
    Values = [documentId,documentAbstractText]
    cursor.execute(SQLCommand,Values)
    documentAbstractId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return documentAbstractId

def InsertDocumentAbstractSentence(documentId,documentAbstractId,documentAbstractSentenceId,documentAbstractSentenceText,documentAbstractSentenceTextBeforeSpellChecking):
    SQLCommand = ("INSERT INTO DocumentAbstractSentences (DocumentId,DocumentAbstractId,DocumentAbstractSentenceId,DocumentAbstractSentenceText,DocumentAbstractSentenceTextBeforeSpellChecking)  VALUES (?,?,?,?,?)")
    Values = [documentId,documentAbstractId,documentAbstractSentenceId,documentAbstractSentenceText,documentAbstractSentenceTextBeforeSpellChecking]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertDocumentAbstractOriginalWords(wordId,originalWord):
    SQLCommand = ("INSERT INTO DocumentAbstractOriginalWords (WordId,OriginalWord)  VALUES (?,?)")
    Values = [wordId,originalWord]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertDocumentAbstractWords(documentId,documentAbstractId,documentAbstractSentenceId,word):
    SQLCommand = ("INSERT INTO DocumentAbstractWords (DocumentId,DocumentAbstractId,DocumentAbstractSentenceId,Word)  VALUES (?,?,?,?)")
    Values = [documentId,documentAbstractId,documentAbstractSentenceId,word]
    cursor.execute(SQLCommand,Values)  
    wordId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return wordId

def InsertGeneratedSummaries(documentId,documentAbstractId,summarizationAlgorithmTypeId,generatedSummaryText):
    try:
        SQLCommand = ("INSERT INTO GeneratedSummaries (DocumentId,DocumentAbstractId,SummarizationAlgorithmTypeId,GeneratedSummaryText)  VALUES (?,?,?,?)")
        Values = [documentId,documentAbstractId,summarizationAlgorithmTypeId,generatedSummaryText]
        cursor.execute(SQLCommand,Values)  
        generatedSummaryId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
        connection.commit()
        return generatedSummaryId
    except Exception as err:
        #generatedSummaryText = FileHelper.ArrangeTextQuotes(generatedSummaryText)
        #SQLCommand = ("INSERT INTO GeneratedSummaries (DocumentId,DocumentAbstractId,SummarizationAlgorithmTypeId,GeneratedSummaryText)  VALUES (?,?,?,?)")
        #Values = [documentId,documentAbstractId,summarizationAlgorithmTypeId,generatedSummaryText]
        #cursor.execute(SQLCommand,Values)  
        #generatedSummaryId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
        #connection.commit()
        return random.randint(10000,100001)

def InsertPerformanceEvaluationResults(documentId,documentAbstractId,successRate,numberOfNamedEntitiesMatched,totalNumberOfNamedEntities,namedEntityAlgorithmTypeId,spellCheckerAlgorithmTypeId,summarizationAlgorithmType,summarizationAlgorithmTypeId,createDate,operationTime):
    SQLCommand = ("INSERT INTO PerformanceEvaluationResults (DocumentId,DocumentAbstractId,SuccessRate,NumberOfNamedEntitiesMatched,TotalNumberOfNamedEntities,NamedEntityAlgorithmTypeId,SpellCheckerAlgorithmTypeId,SummarizationAlgorithmType,SummarizationAlgorithmTypeId,CreateDate,OperationTime)  VALUES (?,?,?,?,?,?,?,?,?,?,?)")
    Values = [documentId,documentAbstractId,successRate,numberOfNamedEntitiesMatched,totalNumberOfNamedEntities,namedEntityAlgorithmTypeId,spellCheckerAlgorithmTypeId,summarizationAlgorithmType,summarizationAlgorithmTypeId,createDate,operationTime]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,documentAbstractSentenceId,entityText,entityCategory,entitySubCategory):
    SQLCommand = ("INSERT INTO DocumentAbstractNamedEntities (DocumentId, DocumentAbstractId,DocumentAbstractSentenceId, EntityText, EntityCategory, EntitySubCategory)  VALUES (?,?,?,?,?,?)")
    Values = [documentId,documentAbstractId,documentAbstractSentenceId,entityText,entityCategory,entitySubCategory]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertSimilarityRateResults(documentId,documentAbstractId,generatedSummaryId,similarityAlgorithmTypeId,similarityRate,createDate,operationTime):
    SQLCommand = ("INSERT INTO SimilarityRateResults (DocumentId,DocumentAbstractId,GeneratedSummaryId,SimilarityAlgorithmTypeId,SimilarityRate,CreateDate,OperationTime)  VALUES (?,?,?,?,?,?,?)")
    Values = [documentId,documentAbstractId,generatedSummaryId,similarityAlgorithmTypeId,similarityRate,createDate,operationTime]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertSentenceSimilarityResults(abstractSentenceId,originalSentenceId,similarityAlgorithmTypeId,similarityRate,createDate):
    SQLCommand = ("INSERT INTO SentenceSimilarityResults (AbstractSentenceId,OriginalSentenceId,SimilarityAlgorithmTypeId,SimilarityRate,CreateDate)  VALUES (?,?,?,?,?)")
    Values = [abstractSentenceId,originalSentenceId,similarityAlgorithmTypeId,similarityRate,createDate]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def InsertWebSearchs(isActive,createDate):
    SQLCommand = ("INSERT INTO WebSearchs (IsActive,CreateDate)  VALUES (?,?)")
    Values = [isActive,createDate]
    cursor.execute(SQLCommand,Values)  
    webSearchId=cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return webSearchId

def InsertVisitedWebSites(webSearchId, url, searchTerm, createDate):
    SQLCommand = ("INSERT INTO VisitedWebSites (WebSearchId, Url, SearchTerm, CreateDate)  VALUES (?,?,?,?)")
    Values = [webSearchId, url, searchTerm, createDate]
    cursor.execute(SQLCommand,Values)  
    visitedWebSiteId = cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]
    connection.commit()
    return visitedWebSiteId

def InsertFinancialTermsDictionary(webSearchId,financialTerm,isActive):
    SQLCommand = ("INSERT INTO FinancialTermsDictionary (WebSearchId,FinancialTerm,IsActive)  VALUES (?,?,?)")
    Values = [webSearchId,financialTerm,isActive]
    cursor.execute(SQLCommand,Values)  
    connection.commit()

def BulkInsertDocumentSentences(documentId, sentenceList):
    sentenceDictList = {}
    lastSentenceId = GetLastIdByGivenTable("Sentences","SentenceId")
    for sentenceId, sentence in enumerate(sentenceList, start=lastSentenceId +1):
        InsertSentence(documentId,sentenceId,sentence,sentence)
        sentenceDictList[sentenceId] = sentence
    return sentenceDictList

def BulkInsertDocumentAbstractSentences(documentId, documentAbstractId,sentenceList):
    sentenceDictList = {}
    lastDocumentAbstractSentenceId = GetLastIdByGivenTable("DocumentAbstractSentences","DocumentAbstractSentenceId")
    for sentenceId, sentence in enumerate(sentenceList, start=lastDocumentAbstractSentenceId +1):
        InsertDocumentAbstractSentence(documentId,documentAbstractId,sentenceId,sentence,sentence)
        sentenceDictList[sentenceId] = sentence
    return sentenceDictList

def BulkInsertFinancialTermsDictionary(webSearchId,financialTermlist):
    for financialTerm in financialTermlist:
        InsertFinancialTermsDictionary(webSearchId,financialTerm,True)

def TruncateWordsTable():
    SQLCommand = ("Truncate table Words")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateOriginalWordsTable():
    SQLCommand = ("Truncate table OriginalWords")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentsTable():
    SQLCommand = ("Truncate table Documents")
    cursor.execute(SQLCommand)
    connection.commit()
    
def TruncateNamedEntitiesTable():
    SQLCommand = ("Truncate table NamedEntities")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateSentencesTable():
    SQLCommand = ("Truncate table Sentences")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentAbstractsTable():
    SQLCommand = ("Truncate table DocumentAbstracts")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentAbstractSentencesTable():
    SQLCommand = ("Truncate table DocumentAbstractSentences")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentAbstractOriginalWordsTable():
    SQLCommand = ("Truncate table DocumentAbstractOriginalWords")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentAbstractWordsTable():
    SQLCommand = ("Truncate table DocumentAbstractWords")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncatePerformanceEvaluationResultsTable():
    SQLCommand = ("Truncate table PerformanceEvaluationResults")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateSimilarityRateResultsTable():
    SQLCommand = ("Truncate table SimilarityRateResults")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateGeneratedSummariesTable():
    SQLCommand = ("Truncate table GeneratedSummaries")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateSentenceSimilarityResultsTable():
    SQLCommand = ("Truncate table SentenceSimilarityResults")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateDocumentAbstractNamedEntitiesTable():
    SQLCommand = ("Truncate table DocumentAbstractNamedEntities")
    cursor.execute(SQLCommand)
    connection.commit()

def TruncateAllTables():
    TruncateWordsTable()
    TruncateOriginalWordsTable()
    TruncateNamedEntitiesTable()
    TruncateDocumentsTable()
    TruncateSentencesTable()
    TruncateDocumentAbstractsTable()
    TruncateDocumentAbstractSentencesTable()
    TruncateDocumentAbstractOriginalWordsTable()
    TruncateDocumentAbstractWordsTable()
    TruncatePerformanceEvaluationResultsTable()
    TruncateSimilarityRateResultsTable()
    TruncateGeneratedSummariesTable()
    TruncateSentenceSimilarityResultsTable()
    TruncateDocumentAbstractNamedEntitiesTable()

connection = pypyodbc.connect('Driver={SQL Server};'
                                              'Server=NB-200586;'
                                               'Database=DocumentVerification;') 

cursor = connection.cursor()