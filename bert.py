from summarizer import Summarizer

def GenerateSummary(text,topSentenceCount):
    model = Summarizer()
    summarySentences = model(text,num_sentences=topSentenceCount)
    summary = ' '.join(summarySentences)
    return summary

#Usage -->
#References: https://pypi.org/project/bert-extractive-summarizer/
#import FileHelper
#import DataPreprocessingHelper
#topSentenceCount = 5
#fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\001.txt"
#fullText = FileHelper.GetDocumentContentByGivenPath(fullTextPath)
#fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
#print("Full Text: \n" +fullText)
#summaryText = GenerateSummary(fullText,topSentenceCount)
#print("Summary Text: \n" + summaryText)

