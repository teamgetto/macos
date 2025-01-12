from gensim.summarization import summarize
#from gensim.summarization import keywords

import FileHelper
import DataPreprocessingHelper

#from gensim.summarization import summarize

#print(summarize(DOCUMENT, ratio=0.2, split=False))

def GenerateSummary(text,summaryRatio,summaryWordCount):
    summary= ""
    if summaryRatio>0:
        summary= summarize(text, ratio = summaryRatio)
    elif summaryWordCount>0:
        summary = summarize(text, word_count = summaryWordCount)

    return summary


top_n = 3
fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\001.txt"
fullText = FileHelper.GetDocumentContentByGivenPath(fullTextPath)
fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
print("Full Text: \n" +fullText)
summaryText = GenerateSummary(fullText,0.3,0)
print("Summary Text: \n" + summaryText[0])

#Reference: https://www.geeksforgeeks.org/python-extractive-text-summarization-using-gensim/
