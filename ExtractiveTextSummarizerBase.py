import datetime
import SumyTextRankExtractiveSummarizer
import SumyLexRankExtractiveSummarizer
import SumyLsaExtractiveSummarizer
import SumyKLDivergenceExtractiveSummarizer
import TextRankExtractiveSummarizer
import SentenceFrequencyBasedExtractiveSummarizer
import HelmholtzPrincipleBasedExtractiveSummarizer
import TransformerExtractiveSummarizer
import HuggingFacesTransformersExtractiveSummarizer
import DataPreprocessingHelper
import LogHelper
import HtmlDataHelper
import FileHelper
import SpellCheckerBase
import NamedEntityRecognizerBase
import os
import DbHelper
import ExtractiveTextSummarizationAlgorithmType

def SummarizeDocumentByGivenAlgorithmType(text,extractiveTextSummarizationAlgorithmTypeId,topSentenceCount):
    summaryText = ""
    if extractiveTextSummarizationAlgorithmTypeId == ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.SentenceFrequencyBasedExtractiveTextSummarizer.value:
        summaryText = SentenceFrequencyBasedExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId ==ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.SumyKLDivergenceExtractiveSummarizer.value:
        summaryText = SumyKLDivergenceExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId ==ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.SumyLexRankExtractiveSummarizer.value:
        summaryText = SumyLexRankExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId ==ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.SumyLsaExtractiveSummarizer.value:
        summaryText = SumyLsaExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId ==ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.SumyTextRankExtractiveSummarizer.value:
        summaryText = SumyTextRankExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId ==ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.TextRankExtractiveSummarizer.value:
        summaryText = TextRankExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId == ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.HelmholtzPrincipleBasedExtractiveSummarizer.value:
        summaryText = HelmholtzPrincipleBasedExtractiveSummarizer.GenerateSummary(text,topSentenceCount)
    elif extractiveTextSummarizationAlgorithmTypeId == ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.TransformerExtractiveSummarizer.value:
        summaryText = TransformerExtractiveSummarizer.GenerateSummary(text,topSentenceCount) 
    elif extractiveTextSummarizationAlgorithmTypeId == ExtractiveTextSummarizationAlgorithmType.ExtractiveTextSummarizationAlgorithmType.HuggingFacesTransformersExtractiveSummarizer.value:
        summaryText = HuggingFacesTransformersExtractiveSummarizer.GenerateSummary(text,topSentenceCount) 
    return summaryText