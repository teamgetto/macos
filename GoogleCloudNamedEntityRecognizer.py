#import argparse

#from google.cloud import language
#from google.cloud.language import enums
#from google.cloud.language import types


#def main(text):
#    client = language.LanguageServiceClient()

#    document = types.Document(
#        content=text,
#        type=enums.Document.Type.PLAIN_TEXT)

#    entities = client.analyze_entities(document=document).entities

#    # entity types from enums.Entity.Type
#    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
#                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER', 'PHONE_NUMBER', 'ADDRESS', 'DATE', 'NUMBER', 'PRICE')

#    for entity in entities:
#        print('=' * 20)
#        print('         name: {0}'.format(entity.name))
#        print('         type: {0}'.format(entity_type[entity.type]))
#        print('     salience: {0}'.format(entity.salience))
#        print('wikipedia_url: {0}'.format(entity.metadata.get('wikipedia_url', '-')))


#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument('text', help='The text you\'d like to analyze entities.')
#    args = parser.parse_args()
#    main(args.text)


from google.cloud import language_v1
from google.oauth2 import service_account

#client = language.LanguageServiceClient(credentials=credentials)

def sample_analyze_entities(text_content):
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    #client = language_v1.LanguageServiceClient()
    credentials = service_account.Credentials.from_service_account_file("C:\\Users\\TFKB\\Desktop\\PAPERS\\PHD\\ThesisAlgorithmModels\\GoogleCloud\\phdthesisdocumentverification.json")
    client = language_v1.LanguageServiceClient(credentials=credentials)
    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))

sentence = "Football and baseball have been locked in a perpetual battle for the affection of sports in the United States."
sample_analyze_entities(sentence)
