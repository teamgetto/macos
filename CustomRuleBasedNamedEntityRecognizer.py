import re
 
# Function to find currency symbol
# in a text using regular expression
def findCurrencySymbol(text):
 
    # Regex to find any currency
    # symbol in a text
    regex = "\\$|\\£|\\€"
 
    for m in re.finditer(regex, text):
        print(text[m.start(0)], "-" ,m.start(0))
 

def FindNumber(text):
    result = [int(i) for i in text.split() if i.isdigit()]
    print("The numbers list is : " + str(result))


text = "$27 - $21.30equal to $5.70"
findCurrencySymbol(text)
FindNumber(text)