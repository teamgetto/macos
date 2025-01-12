from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import LogHelper

key = "81c0eee7e5b3469093a3619da1e927cf"
endpoint = "https://phdazuretextanalytics.cognitiveservices.azure.com/"

def AuthenticateClient():
    azureKeyCredential = AzureKeyCredential(key)
    textAnalyticsClient = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=azureKeyCredential)
    return textAnalyticsClient

def AnalysisSentence(text):
    authenticateClient =AuthenticateClient()
    documents = [text]
    response = authenticateClient.analyze_sentiment(documents=documents)[0]
    LogHelper.PrintInfoLog("Document Sentiment: {}".format(response.sentiment))
    LogHelper.PrintInfoLog("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        LogHelper.PrintInfoLog("Sentence: {}".format(sentence.text))
        LogHelper.PrintInfoLog("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
        LogHelper.PrintInfoLog("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))