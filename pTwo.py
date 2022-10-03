import sys
import os
import re
import pickle
import nltk
import math


def check_answers():
    testfile = open('LangId.sol')
    results_file = open('LangId.results')
    testLine = testfile.readline()
    guess = results_file.readline()
    Corr_guesses = {'English\n': 0, 'French\n': 0, 'Italian\n': 0}
    totals = {'English\n': 0, 'French\n': 0, 'Italian\n': 0}
    incorr_guesses = {'English\n': [], 'French\n': [], 'Italian\n': []}
    while testLine:
        test = testLine.split(' ')[1]
        totals[test] += 1
        if test == guess:
            Corr_guesses[test] += 1
        else:
            incorr_guesses[test].append(testLine.split(' ')[0])
        testLine = testfile.readline()
        guess = results_file.readline()
    return Corr_guesses['English\n']/totals['English\n'], Corr_guesses['French\n']/totals['French\n']\
        , Corr_guesses['Italian\n']/totals['Italian\n'], incorr_guesses

def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)

    unigrams_test = nltk.word_tokenize(text)
    unigrams_test = [t.lower() for t in unigrams_test]
    bigrams_test = list(nltk.ngrams(unigrams_test, 2))

    p_laplace = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace


def get_counts(filename, unigram_dict):
    file = open(filename, 'r', encoding="utf8")
    raw_text = file.read()
    unigrams = nltk.word_tokenize(raw_text)
    file.close()
    return len(unigrams), len(unigram_dict)


if __name__ == '__main__':

    Eng_uniDict = pickle.load(open('Eng_uniDict.p', 'rb'))
    Eng_biDict = pickle.load(open('Eng_biDict.p', 'rb'))
    Fre_uniDict = pickle.load(open('Fre_uniDict.p', 'rb'))
    Fre_biDict = pickle.load(open('Fre_biDict.p', 'rb'))
    Ita_uniDict = pickle.load(open('Ita_uniDict.p', 'rb'))
    Ita_biDict = pickle.load(open('Ita_biDict.p', 'rb'))

    Eng_N, Eng_V = get_counts('LangId.train.English', Eng_uniDict)
    Fre_N, Fre_V = get_counts('LangId.train.French', Fre_uniDict)
    Ita_N, Ita_V = get_counts('LangId.train.Italian', Ita_uniDict)

    test_file = open('LangId.test', 'r')
    text_in = test_file.readline()

    res_file = open('LangId.results', 'w')

    while text_in:
        eng_prob = compute_prob(text_in, Eng_uniDict, Eng_biDict, Eng_N, Eng_V)
        fre_prob = compute_prob(text_in, Fre_uniDict, Fre_biDict, Fre_N, Fre_V)
        ita_prob = compute_prob(text_in, Ita_uniDict, Ita_biDict, Ita_N, Ita_V)
        if eng_prob > fre_prob and eng_prob > ita_prob:
            res_file.write('English\n')
        elif fre_prob > eng_prob and fre_prob > ita_prob:
            res_file.write('French\n')
        else:
            res_file.write('Italian\n')
        text_in = test_file.readline()
    res_file.close()

    Eng_Acc, Fre_Acc, Ita_Acc, wrong_ans = check_answers()
    print('English Accuracy = ' + str(Eng_Acc))
    print('Misidentified lines : ')
    for i in wrong_ans['English\n']:
        print(i)
    print('French Accuracy = ' + str(Fre_Acc))
    print('Misidentified lines : ')
    for i in wrong_ans['French\n']:
        print(i)
    print('Italian Accuracy = ' + str(Ita_Acc))
    print('Misidentified lines : ')
    for i in wrong_ans['Italian\n']:
        print(i)