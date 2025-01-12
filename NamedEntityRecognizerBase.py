import SpacyNamedEntityRecognizer
import StanfordUniversityNamedEntityRecognizer
import NltkNamedEntityRecognizer
import NlpCloudNamedEntityRecognizer
import MonkeyLearnNamedEntityRecognizer
import AzureCognitiveServiceNamedEntityRecognizer
import BertBaseTurkishNamedEntityRecognizer
import DbHelper
import NamedEntityAlgorithmType

def FindAndSaveDBNamedEntitiesByGivenAlgorithmType(documentId,documentAbstractId,sentenceId,namedEntityAlgorithmTypeId,isFullTextDocument):
    if isFullTextDocument == True:
        sentence = DbHelper.GetOriginalDocumentSentenceTextById(documentId, sentenceId)
    else:
        sentence = DbHelper.GetAbstractDocumentSentenceTextById(documentId, documentAbstractId, sentenceId)

    if namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.AzureCognitiveServiceNamedEntityRecognizer.value:
        namedEntities = AzureCognitiveServiceNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities:
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity.text,namedEntity.category, namedEntity.subcategory)
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity.text,namedEntity.category,namedEntity.subcategory)
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.BertBaseTurkishNamedEntityRecognizer.value:
        namedEntities = BertBaseTurkishNamedEntityRecognizer.FindNamedEntities(sentence) 
        for namedEntity in namedEntities:
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity.text,namedEntity.label_, "-")
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity.text,namedEntity.label_, "-")
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.StanfordUniversityNamedEntityRecognizer.value:
        namedEntities = StanfordUniversityNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities:
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity[0],namedEntity[1], "-")
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity[0],namedEntity[1], "-")
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.NltkNamedEntityRecognizer.value:
        namedEntities = NltkNamedEntityRecognizer.FindNamedEntities(sentence) 
        for namedEntity in namedEntities:
            entityText =' '.join(entity[0] for entity in namedEntity)
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,entityText,namedEntity.label(), "-")   
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,entityText,namedEntity.label(), "-")
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.NlpCloudNamedEntityRecognizer.value:
        namedEntities = NlpCloudNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities:
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity["text"],namedEntity["type"], "-") 
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity["text"],namedEntity["type"], "-")
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.MonkeyLearnNamedEntityRecognizer.value:
        namedEntities = MonkeyLearnNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities['extractions']:
            if isFullTextDocument ==True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity["extracted_text"],namedEntity["tag_name"], "-")
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity["extracted_text"],namedEntity["tag_name"], "-")
    elif namedEntityAlgorithmTypeId == NamedEntityAlgorithmType.NamedEntityAlgorithmType.SpacyNamedEntityRecognizer.value:
        namedEntities = SpacyNamedEntityRecognizer.FindNamedEntities(sentence)
        for namedEntity in namedEntities:
            if isFullTextDocument == True:
                DbHelper.InsertNamedEntity(documentId,sentenceId,namedEntity.text,namedEntity.label_, "-")
            else:
                DbHelper.InsertDocumentAbstractNamedEntities(documentId,documentAbstractId,sentenceId,namedEntity.text,namedEntity.label_, "-")

    return namedEntities