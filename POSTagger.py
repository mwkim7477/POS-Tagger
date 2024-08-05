#POS Tagger
import string, math

def applypostagging(keywordsentencedict):
    #Grab training counts
    trainset = open("POS.train.large",'r')
    postoworddict = {}
    vocab = []
    for line in trainset:
        line = line.split(" ")
        for wordposinstance in line:
            word = wordposinstance[:wordposinstance.rindex("/")]
            vocab.append(word)
            #split | to account for multiple pos tags
            pos = wordposinstance[wordposinstance.rindex("/") + 1:].split("|")
            #Account for multiple POS tags
            for individualpos in pos:
                if individualpos not in postoworddict:
                    postoworddict[individualpos] = {}
                elif word in postoworddict[individualpos]:
                    postoworddict[individualpos][word] += 1
                else:
                    postoworddict[individualpos][word] = 1
                    
    #Unique vocab
    vocab = list(set(vocab))

    totalpostags = 0
    for key in postoworddict.keys():
        totalpostags += sum(postoworddict[key].values())

    #Iterate through each of the sentences containing a keyword
    for keyword in keywordsentencedict:
        sentenceslist = keywordsentencedict[keyword]
        #Iterate through each sentence
        for sentence in sentenceslist:
            sentencetags = []
            wordslst = sentence.split(" ")
            for word in wordslst:
                newword = [word]
                #Split punctuation if it exists
                if any(c for c in word for c in string.punctuation):
                    #Parse punctuation
                    newword = ""
                    for c in word:
                        if c in string.punctuation:
                            newword = newword + " " + c + " "
                        else:
                            newword = newword + c
                    newword = newword.split(" ")
                scores = []
                for pos in postoworddict.keys():
                    conditionals = []
                    for token in newword:
                        if word not in postoworddict[pos]:
                            wordoccurenceinpos = 0
                        else:
                            wordoccurenceinpos = postoworddict[pos][word]
                        wordconditionalprob = float(wordoccurenceinpos + 1) / float(sum(postoworddict[pos].values()) + len(vocab))
                        #Use log space in base 10
                        wordconditionalprob = math.log10(wordconditionalprob)
                        conditionals.append(wordconditionalprob) 
                    sumconditionals = sum(conditionals)
                    probabilitypos = math.log10(float(sum(postoworddict[pos].values())) / float(totalpostags))
                    score = sumconditionals + (probabilitysense)
                    #Append to scores list
                    scores.append([score, pos])
                predictedpos = max(scores)[1]
                sentencetags.append(predictedpos)
            #Split just incase of multiple words
            wordsinkey = keyword.split(" ")
            tokensfromkeyword = []
            for word in wordsinkey:
                newword = [word]
                #Split punctuation if it exists
                if any(c for c in word for c in string.punctuation):
                    #Parse punctuation
                    newword = ""
                    for c in word:
                        if c in string.punctuation:
                            newword = newword + " " + c + " "
                        else:
                            newword = newword + c
                    newword = newword.split(" ")
                tokensfromkeyword.append(newword)
            startingindexofkeyword = sentence.find(keyword)
            tokenindices = [startingindexofkeyword + i for i in range(0, len(tokensfromkeyword))]
            nounadjectiveverb = False
            for i in tokenindices:
                if 'NN' == sentencetags[i] or 'JJ' == sentencetags[i] or 'VB' == sentencetags[i] or 'VBD' == sentencetags[i] or 'VBG' == sentencetags[i] or 'VBN' == sentencetags[i] or 'VBP' == sentencetags[i] or 'VBZ' == sentencetags[i]:
                    nounadjectiveverb = True
            if nounadjectiveverb == False:
                sentenceslist.remove(sentence)                
        keywordsentencedict[keyword] = len(sentenceslist)
    return keywordsentencedict
