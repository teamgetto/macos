from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk.data         
import nltk
import string
from string import punctuation
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk import wordpunct_tokenize
from collections import Counter
from nltk.stem import WordNetLemmatizer 
import string
import re

#nltk.download('wordnet')      #download if using this module for the first time
#nltk.download('stopwords')    #download if using this module for the first time

def GetCleanedWordsByGivenSentence(sentence):
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(sentence)
    words = [word.translate(translator) for word in words]
    #words = [word for word in words if len(word) > 1] # Bu kısım özellikle kapatıldı. Tek haneli sayılar çıkarılıyor.
    #words = [word for word in words if not word.isnumeric()] # Bu kısım özellikle kapatıldı. Sayılar çıkarılıyor.
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords.words('english')]  
    words= [word for word in words if word != ""]
    return words

def GetWordListByGivenText(text):
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(text)
    words = [word.translate(translator) for word in words]
    words = [word for word in words if word not in stopwords.words('english')]  
    words= [word for word in words if word != ""]
    return words

def GetNonNumericWordListByGivenText(text):
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(text)
    words = [word.translate(translator) for word in words]
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords.words('english')]  
    words= [word for word in words if word != ""]
    return words


def CleanDocument(document):
    stopWords = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    wordNetLemmatizer = WordNetLemmatizer()
    stopWordRemoval = " ".join([i for i in document.lower().split() if i not in stopWords])
    punctuationRemoval = ''.join(ch for ch in stopWordRemoval if ch not in exclude)
    normalizedDocument = " ".join(wordNetLemmatizer.lemmatize(word) for word in punctuationRemoval.split())
    return normalizedDocument

def RemoveSquareBracketsAndExtraSpaces(document):
    document = re.sub(r'\[[0-9]*\]', ' ', document)  # Sub() ---> Bir metin içerisindeki değeri başka bir değerle değiştirmek için kullanılır.
    document = re.sub(r'\s+', ' ', document)
    return document

def RemoveSpecialCharactersAndDigits(document):
    document = re.sub('[^a-zA-Z]', ' ', document )
    document = re.sub(r'\s+', ' ', document)
    return document
  
def RemoveSpaceCharacterByGivenItemList(itemList):
    innerItemList = []
    for item in itemList:
        pattern = re.compile(r'\s+')
        innerItemList.append(re.sub(pattern, '', item[0]))
    return innerItemList 

def RemoveStripByGivenItemList(itemList):
    innerItemList = []
    for item in itemList:
        innerItemList.append(item[0].strip())
    return innerItemList

def RemoveNewLineCharactersByGivenText(text):
    text = text.replace('\n'," ")
    return text

def RemoveStopwords(text):
    stopWords = set(stopwords.words('english'))
    stopWordRemoval = " ".join([i for i in text if i not in stopWords])
    return stopWordRemoval

def GetEnglishLanguageStopwords():
    stopWords = set(stopwords.words('english'))
    return stopWords