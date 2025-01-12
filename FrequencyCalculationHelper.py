from nltk.corpus import stopwords
import nltk

def GetWordFrequenciesByGivenText(text):
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies

def GetWordFrequenciesByWordList(wordList):
    word_frequencies = {}
    for word in wordList:
        if word not in stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies

from nltk import ngrams

sentence = 'this is a foo bar sentences and i want to ngramize it'

n = 6
sixgrams = ngrams(sentence.split(), n)

for grams in sixgrams:
  print(grams)