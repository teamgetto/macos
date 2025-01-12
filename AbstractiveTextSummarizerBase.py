import datetime
import DataPreprocessingHelper
import LogHelper
import HtmlDataHelper
import FileHelper
import SpellCheckerBase
import NamedEntityRecognizerBase
import os
import DbHelper
import NamedEntityBasedAbstractiveSummarizer
import AbstractiveTextSummarizationAlgorithmType
def SummarizeDocumentByGivenAlgorithmType(fullText,originalAbstractText,abstractiveTextSummarizationAlgorithmTypeId):
    summaryText = ""
    if abstractiveTextSummarizationAlgorithmTypeId == AbstractiveTextSummarizationAlgorithmType.AbstractiveTextSummarizationAlgorithmType.NamedEntityBased.value:
        summaryText = NamedEntityBasedAbstractiveSummarizer.GenerateSummary(text,topSentenceCount)
