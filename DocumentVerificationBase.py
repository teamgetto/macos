from bs4 import BeautifulSoup
import DbHelper
import DataPreprocessingHelper
import StemHelper
import AzureCognitiveServiceNamedEntityRecognizer
import LogHelper
#import NltkNamedEntityRecognizer
#import SpacyNamedEntityRecognizer
#import StanfordUniversityNamedEntityRecognizer
import FileHelper
#import AzureCognitiveServiceSpellChecker
#import TextBlobSpellChecker
#import AutoCorrectSpellChecker
#import SpelloSpellChecher
import datetime
import HtmlDataHelper

#--------------------Steps---------------------------------------

# Dokümanı oku ve db ye kaydet.
# Doküman içerisindeki cümleleri liste olarak döngüye al.
# Döngü ile her bir cümle içerisindeki kelimeleri ön işlemeden geçir ve words tablosuna kaydet.
# Words tablosuna kaydedilen kelimenin ön işlemeden geçirilmiş halinin NER halini bul ve NamedEntities tablosuna kaydet.

#----------------------------------------------------------------

path= "C:\\Users\\TFKB\\Desktop\\Papers\\PHD\\Thesis\\Datasets\\Xml\\DocumentVerificationExampleDocument.xml"
documentTopic = "Sport"
documentSubTopic = "Football"
documentId=1

def Run():
    DbHelper.TruncateAllTables()
    documentText = FileHelper.GetDocumentContentByGivenPath(path)
    documentText=HtmlDataHelper.RemoveHtmlTags(documentText)
    DbHelper.InsertDocument(documentId,path,documentText,documentTopic,documentSubTopic)
    sentences = FileHelper.GetTextSentencesBySpacy(documentText)
    for sentenceId, sentence in enumerate(sentences, start=1):
        #correctedText = AzureCognitiveServiceSpellChecker.SpellChecker(sentence)
        #print(correctedText)
        DbHelper.InsertSentence(documentId,sentenceId,sentence)
        originalWords=DataPreprocessingHelper.GetCleanedWordsByGivenSentence(sentence)
        namedEntities = AzureCognitiveServiceNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities:
            DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity.text,namedEntity.category, namedEntity.subcategory)
        for originalWord in originalWords:
            stem=StemHelper.FindStem(originalWord)
            wordId= DbHelper.InsertWord(documentId,sentenceId,stem)
            DbHelper.InsertOriginalWord(wordId,originalWord)

LogHelper.PrintInfoLog("Uygulama başladı.")
start=datetime.datetime.now()
Run()
end=datetime.datetime.now()
LogHelper.PrintInfoLog("Spello SpellChecker running Time: " + str(end-start))
LogHelper.PrintInfoLog("\n Uygulama tamamlandı.")