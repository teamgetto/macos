from monkeylearn import MonkeyLearn

monkeyLearn = MonkeyLearn("f79ade37b1a97fa40a96109842c1011ecf399825")
modelId = "ex_A9nCcXfn"
externalId= "TFKB"

def FindNamedEntities(text):
    data = ['first text', {'text': text , 'external_id': externalId}, '']
    response = monkeyLearn.extractors.extract(modelId, data=data)
    for res in response.body:
        if res['text'] == text and res['external_id'] == externalId and res["error"] ==False:
            return res

# Usage  -->
# Important  --> Current plan includes 300 queries a month.
#if namedEntityAlgorithmTypeId == 8 :
#    namedEntities = MonkeyLearnNamedEntityRecognizer.FindNamedEntities(fullText)
#    for namedEntity in namedEntities['extractions'] :
#        DbHelper.InsertNamedEntity(documentId,1,namedEntity["extracted_text"],namedEntity["tag_name"], "-") 