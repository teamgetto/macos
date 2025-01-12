from enum import Enum

class ExtractiveTextSummarizationAlgorithmType(Enum):
    SentenceFrequencyBasedExtractiveTextSummarizer = 1
    SumyKLDivergenceExtractiveSummarizer = 2
    SumyLexRankExtractiveSummarizer = 3
    SumyLsaExtractiveSummarizer = 4
    SumyTextRankExtractiveSummarizer = 5
    TextRankExtractiveSummarizer = 6
    HelmholtzPrincipleBasedExtractiveSummarizer = 7
    TransformerExtractiveSummarizer = 8
    HuggingFacesTransformersExtractiveSummarizer = 9