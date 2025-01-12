#from flair.data import Sentence
#from flair.models import SequenceTagger

#def FindNamedEntities(text):
#    sentence = Sentence(text)
#    tagger = SequenceTagger.load('ner')
#    tagger.predict(sentence)
#    print(sentence)
#    print('The following NER tags are found:')
#    for entity in sentence.get_spans('ner'):
#        print(entity)

sentence = "Football and baseball have been locked in a perpetual battle for the affection of sports in the United States."
FindNamedEntities(sentence)
# References: https://github.com/flairNLP/flair

#Error: 
#WARNING: Ignoring invalid distribution -ensorflow (c:\program files\python37\lib\site-packages)
#ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. 
#This behaviour is the source of the following dependency conflicts.
#tensorboard 2.4.1 requires google-auth<2,>=1.6.3, but you have google-auth 2.2.1 which is incompatible.
#google-colab 1.0.0 requires google-auth~=1.4.0, but you have google-auth 2.2.1 which is incompatible.
#google-colab 1.0.0 requires requests~=2.21.0, but you have requests 2.26.0 which is incompatible.
#google-colab 1.0.0 requires six~=1.12.0, but you have six 1.15.0 which is incompatible.
#contextualspellcheck 0.4.1 requires spacy>=3.0.0, but you have spacy 2.2.2 which is incompatible.