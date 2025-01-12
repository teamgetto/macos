from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import LogHelper

#key = "81c0eee7e5b3469093a3619da1e927cf"
key = "28fa70b114244dfabded41d02b05f9aa"
#endpoint = "https://phdazuretextanalytics.cognitiveservices.azure.com/"
endpoint = "https://phdazurecognitiveservices.cognitiveservices.azure.com/"

def AuthenticateClient():
    azureKeyCredential = AzureKeyCredential(key)
    textAnalyticsClient = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=azureKeyCredential)
    return textAnalyticsClient

def FindNamedEntities(text):
    authenticateClient = AuthenticateClient()
    try:
        documents = [text]
        result = authenticateClient.recognize_entities(documents = documents)[0]
        #LogHelper.PrintInfoLog("Recognized Named Entities by Using Azure Cognitive Services:\n")
        for entity in result.entities:
            if type(entity.subcategory) == type(None):
                entity.subcategory ="Unknown"
            #entityConfidenceScore = round(entity.confidence_score, 2)
            #entityLength = entity.length
            #entityOffset = entity.offset
            #LogHelper.PrintInfoLog("\tText: \t" + entity.text + "\tCategory: \t" + entity.category + "\tSubCategory: \t" + entity.subcategory +
            #        "\n\tConfidence Score: \t" + str(entityConfidenceScore) + "\tLength: \t" + str(entityLength) + "\tOffset: \t" + str(entityOffset) + "\n")

        return result.entities

    except Exception as err:
        LogHelper.PrintErrorLog("Encountered exception in Azure Cognitive Services {}".format(err))

#References: https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/named-entity-recognition/quickstart?pivots=programming-language-python
#https://portal.azure.com/#@ahmettoprakturkiyefinanscom.onmicrosoft.com/resource/subscriptions/a0dd62d8-bd15-47d7-b6fb-4a2a66af6bd0/resourceGroups/AhmetToprakResource/providers/Microsoft.CognitiveServices/accounts/PhdAzureCognitiveServices/cskeys