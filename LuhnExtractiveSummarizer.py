from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

summarizer = LuhnSummarizer()

def GenerateSummary(text,sentenceCount):
    summary= ""
    parser=PlaintextParser.from_string(text,Tokenizer("english"))
    summary = summarizer(parser.document,sentenceCount)
    for sentence in summary:
        summary += sentence
    return summary

#References: https://www.machinelearningplus.com/nlp/text-summarization-approaches-nlp-example/
# https://www.projectpro.io/article/text-summarization-python-nlp/546