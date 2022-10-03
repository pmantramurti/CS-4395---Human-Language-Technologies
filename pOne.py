import pickle
import nltk


def procFile(filename):
    file = open(filename, 'r', encoding="utf8")
    raw_text = file.read()
    raw_text = raw_text.strip()
    uniDict = {}
    biDict = {}
    unigrams = nltk.word_tokenize(raw_text)
    unigrams = [t.lower() for t in unigrams]
    bigrams = [(unigrams[k], unigrams[k + 1]) for k in range(len(unigrams) - 1)]
    for i in range(0, len(unigrams)):
        if unigrams[i] in uniDict:
            uniDict[unigrams[i]] += 1
        else:
            uniDict[unigrams[i]] = 1
        if i < len(unigrams) - 1:
            if (unigrams[i], unigrams[i+1]) in biDict:
                biDict[(unigrams[i], unigrams[i+1])] += 1
            else:
                biDict[(unigrams[i], unigrams[i + 1])] = 1
    return uniDict, biDict

if __name__ == '__main__':
    Eng_uniDict, Eng_biDict = procFile('LangId.train.English')
    Fre_uniDict, Fre_biDict = procFile('LangId.train.French')
    Ita_uniDict, Ita_biDict = procFile('LangId.train.Italian')
    print(Eng_biDict)
    pickle.dump(Eng_uniDict, open('Eng_uniDict.p', 'wb'))
    pickle.dump(Eng_biDict, open('Eng_biDict.p', 'wb'))
    pickle.dump(Fre_uniDict, open('Fre_uniDict.p', 'wb'))
    pickle.dump(Fre_biDict, open('Fre_biDict.p', 'wb'))
    pickle.dump(Ita_uniDict, open('Ita_uniDict.p', 'wb'))
    pickle.dump(Ita_biDict, open('Ita_biDict.p', 'wb'))