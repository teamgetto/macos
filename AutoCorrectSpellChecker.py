from autocorrect import Speller

def SpellChecker(sentence):
    spell = Speller(lang='en')
    return spell(sentence)

# Usage -->
sentence = "Footbal and basebal hav been lockd in a perpetal battle for the afection of sports in the United States."
print("Sentence before spellchecker  --> " + sentence)
print("Sentence after spellchecker  --> " + SpellChecker(sentence))