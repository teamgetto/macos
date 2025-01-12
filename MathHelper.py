import math
from math import factorial

def CalculateFactorial(number):
    return factorial(number)

def CalculateLog(number):
    return math.log(number)

def CalculateDivision(number1,number2):
    if number2==0:
        number2=1
    return float(number1/number2)

def GetMajorityCountByGivenThreshold(threshold):
    return int(threshold/2 + 1)

def CalculateMultiply(number1,number2):
    return float(number1 * number2)

#totalSimilarityRate = 6.772727272727272
#totalSentence = 156
#averageSimilarityRate = CalculateDivision(totalSimilarityRate, totalSentence)
#print(averageSimilarityRate)