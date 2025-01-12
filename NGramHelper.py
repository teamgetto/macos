from ngram import NGram

def CalculateUniGram(word1,word2):
    score = NGram.compare(word1, word2, N=1)
    return score
    
def CalculateBiGram(word1,word2):
    score = NGram.compare(word1, word2,N=2)
    return score
    
def CalculateTriGram(word1,word2,word3):
    score = NGram.compare(word1, word2,N=3)
    return score


#Usage -->
#w1 = "balance"
#w2 = "finance"
#w3 = "money"

#u = CalculateUniGram(w1,w2)
#b = CalculateBiGram(w1,w2)
#t = CalculateTriGram(w1,w2,w3)
#print(u)
#print(b)
#print(t)
#References: https://pythonhosted.org/ngram/ngram.html