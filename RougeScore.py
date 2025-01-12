from rouge import Rouge
from rouge_score import rouge_scorer


def CalculateSimilarity(mainSentence,searchSentence):
    rougeSimilarity = float(0.0)
    try:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(mainSentence, searchSentence)
        return scores['rouge1'].precision
    except Exception as err:
        return rougeSimilarity

mainSentence = """
A 4-year-old boy is the latest victim of a man-eating leopard, a local police chief says. He suspects one leopard is behind the deaths of 15 people in the past 15 months. A reward has been offered to anyone who captures or kills the man-eating creature. 
"""
searchSentence = """
The police chief suspects a single man-eating leopard is responsible for the deaths. A leopard may have killed 15 people in Nepal in a 15-month span, its latest victim is a 4-year-old boy . The leopard dragged the boy away into the jungle to eat .The grisly discovery marks the 15th victim in the past 15 months in the remote district of western Nepal. Mr. Kharel said he feared the actual number of people killed by the leopard could be higher than 15. Others have lost their lives to leopard attacks in Uttarkhand state in northern India, which borders the Baitadi district. Kharel says he feared others have also lost their life in the area . If not, there are at most two of the man-eating creatures around, he believes.More human victimities could also be expected if more were available to eat more people.
"""

value = CalculateSimilarity(mainSentence, searchSentence)
print(value)