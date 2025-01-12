import re
import pandas as pd
import bs4
import requests
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_lg')

from spacy.matcher import Matcher 
from spacy.tokens import Span 

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)

candidate_sentences = pd.read_csv("C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\ThesisBigDatasets\\WikipediaSentences\\wiki_sentences_v2.csv")
candidate_sentences.shape
candidate_sentences['sentence'].sample(5)



#References: https://www.kaggle.com/pavansanagapati/knowledge-graph-nlp-tutorial-bert-spacy-nltk
# https://www.kaggle.com/pavansanagapati/knowledge-graph-nlp-tutorial-bert-spacy-nltk/notebook