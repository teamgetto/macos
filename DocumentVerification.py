from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk.data
import pypyodbc
import re
import os         
import nltk
import string
from string import punctuation
from nltk.corpus import wordnet
from nltk.corpus import words
import datetime
from autocorrect import spell
import math
from nltk import wordpunct_tokenize
import colorama
from colorama import Fore, Back, Style
from math import factorial
import spacy
import DbHelper
import LogHelper
colorama.init()

def SeparateWordAndSaveDB():
    DbHelper.TruncateAllTables()
    LogHelper.PrintInfoLog("Tüm tablolar truncate edildi.")
    counts = dict()
    paraghraphId = 0
    path= "C:\\Users\\TFKB\\Desktop\\Papers\\PHD\\Thesis\XML\\"
    sortlist = sorted(os.listdir(path))   
    if len(sortlist)==0:
        LogHelper.PrintInfoLog(path+ " adresinde doküman bulunmamaktadır.")
        return
    i = 0
    documentCount=str(len(sortlist))
    LogHelper.PrintInfoLog(path +" adresinde toplam "+ documentCount+ " adet doküman bulunmaktadır.")
    while(i < len(sortlist)):
        LogHelper.PrintInfoLog(str(i)+". sıradaki " + sortlist[i]+ " doküman okunmaya başlandı.")
        dna = open(path + "\\" + sortlist[i],encoding='utf8',errors='ignore')
        try:
            soup = BeautifulSoup(dna)
        except Exception as e:
            LogHelper.PrintErrorLog(sortlist[i]+" dokümanında hata oluştu. Hata " + str(e))
        paragraphs = soup.find_all("p")
        paraghraphId = 1
        stemmer = PorterStemmer()
        for element in paragraphs:           
            tokens = GetContentFreq(element.text)
            tagged = pos_tag(tokens)
            nouns = [word for word,pos in tagged \
	            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]	           
            for word in nouns:
                originalWord=word
                stems = stemmer.stem(word)
                try:
                    DbHelper.InsertOriginalWord(stems,originalWord)
                except Exception as e:
                    LogHelper.PrintErrorLog("OriginalWords tablosuna insert ederken hata oluştu. Hata :" +str(e))

                if stems in counts.keys():
                    shortest,count = counts[stems]
                    counts[stems] = (shortest,count + 1)
                else:
                    counts[stems] = (stems,1)
            for kok in counts:          
                shortest,count = counts[kok]
                try:
                        DbHelper.InsertWord(i,shortest,count,kok,paraghraphId)
                except Exception as e:
                    LogHelper.PrintErrorLog("Words tablosuna insert ederken oluştu. Hata : "+ str(e))

            counts.clear()
            tokens.clear()
            nouns.clear()
            paraghraphId+=1

            number_of_rows_Words = DbHelper.GetWordsCountByDocumentId(i)

        if len(paragraphs)>0 and number_of_rows_Words>0:
            DbHelper.InsertDocument(i,sortlist[i],sortlist[i],sortlist[i])
        i+=1


def GetContentFreq(content):
    translator = str.maketrans('', '', string.punctuation)
    words = nltk.word_tokenize(content)
    words = [word.translate(translator) for word in words]
    words = [word for word in words if len(word) > 1]
    words = [word for word in words if not word.isnumeric()]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stopwords.words('english')]  
    words= [word for word in words if word != ""]
    return words



#SeparateWordAndSaveDB()