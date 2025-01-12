from transformers import pipeline
import FileHelper

def GenerateSummary(text,topSentenceCount):
    summarization = pipeline("summarization")
    summary_text = summarization(text, min_length =50, max_length =1000)[0]['summary_text']
    sentences = FileHelper.GetTextSentencesBySpacy(summary_text)
    if len(sentences) < topSentenceCount:
        return summary_text
    else:
        topSentencesText = ""
        iteration=0
        for sentence in sentences:
            topSentencesText += sentence
            iteration +=1
            if topSentenceCount == iteration:
                return topSentencesText

#Usage -->
#References: https://www.thepythoncode.com/article/text-summarization-using-huggingface-transformers-python
#topSentenceCount = 5
#fullTextPath = "C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\Thesis\\Datasets\\Txt\\BBC News\\Sample10\\Full Text\\001.txt"
#fullText = FileHelper.GetDocumentContentByGivenPath(fullTextPath)
#fullText = DataPreprocessingHelper.RemoveNewLineCharactersByGivenText(fullText)
#print("Full Text: \n" +fullText)
#summaryText = GenerateSummary(fullText,topSentenceCount)
#print("Summary Text: \n" + summaryText)