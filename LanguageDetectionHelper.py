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

def DetectLanguage(text):
    authenticateClient =AuthenticateClient()
    try:
        documents = [text]
        response = authenticateClient.detect_language(documents = documents, country_hint = 'us')[0]
        LogHelper.PrintInfoLog("Language: ", response.primary_language.name)

        return response.primary_language.name

    except Exception as err:
        LogHelper.PrintErrorLog("Encountered exception. {}".format(err))