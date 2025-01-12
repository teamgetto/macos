from enum import Enum

class NamedEntityAlgorithmType(Enum):
    AzureCognitiveServiceNamedEntityRecognizer = 1
    BertBaseTurkishNamedEntityRecognizer = 2
    MonkeyLearnNamedEntityRecognizer = 3
    NlpCloudNamedEntityRecognizer = 4
    NltkNamedEntityRecognizer = 5
    SpacyNamedEntityRecognizer = 6
    StanfordUniversityNamedEntityRecognizer = 7