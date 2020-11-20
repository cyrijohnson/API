from multi_rake import Rake

def getKeywords(text):
    tokens = text.split()
    processedTokens = []
    if len(tokens) < 3:
        processedTokens = text.split()
    else:
        rake = Rake()
        keywords = rake.apply(text)
        for i in keywords:
            tempHold = i[0].split()
            for j in tempHold:
                processedTokens.append(j)
    return processedTokens

