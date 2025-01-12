import boto3
import json
import LogHelper

def FindNamedEntities(sentence):
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
    comprehend = boto3.client(service_name='comprehend', region_name='region')
    LogHelper.PrintInfoLog("Calling DetectEntities")
    LogHelper.PrintInfoLog(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    LogHelper.PrintInfoLog('End of DetectEntities\n')

## Usage --->
#sentence = "Football and baseball have been locked in a perpetual battle for the affection of sports in the United States."
#entities = FindNamedEntities(sentence)