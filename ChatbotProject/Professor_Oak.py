import os
import re
import string

import numpy as np
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import random


def perform_lemmatization(tokens):
    wnlemmatizer = nltk.stem.WordNetLemmatizer()
    return [wnlemmatizer.lemmatize(token) for token in tokens]


def get_processed_text(document):
    punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

#
def generate_response(user_input, pokNames, pokKBase):
    ProfOak_response = ''
    stop_words = set(stopwords.words('english'))
    trainer_q = user_input
    pokName = ''
    for word in trainer_q.split():
        word = re.sub(r'[^\w\s]', '', word)
        if word in [x.lower() for x in pokNames]: # Check which pokemon is being asked about
            pokName = word
    if pokName == '':
        ProfOak_response = 'I\'m quite sorry, young trainer, but I only know about Gen 1 pokemon.' + \
                           '\nProfessor Oak : If you have any questions in my area of expertise, please do relay them to me.'
        return ProfOak_response
    trainer_q = ' '.join([word for word in trainer_q.split() if word not in stop_words and word != pokName]) # get the keywords from the query string
    tempKBase = pokKBase[pokName.capitalize()]
    tempKBase.append(user_input)
    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(tempKBase) # vectorize the knowledge base specific to the pokemon in query
    vectors = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    ans_option = vectors.argsort()[0][-2] # sort sentence vectors by similarity to query, save most similar as answer

    matched_vector = vectors.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2] # check if selected answer is actually related to query

    if vector_matched == 0: # if unrelated, inform user to try again
        ProfOak_response = 'I\'m quite sorry, young trainer, but I only know about Gen 1 pokemon. ' \
                           + '\nProfessor_Oak : If you have any questions in my area of expertise, please do relay them to me.'
        tempKBase.remove(user_query)
        return ProfOak_response
    else:
        ProfOak_response = np.array(tempKBase)[ans_option] # return selected answer to query
        tempKBase.remove(user_query)
        return ProfOak_response


if __name__ == '__main__':
    pokemon_KBase = {}
    if os.path.isfile('Pokemon_KnowledgeBase.p'):
        pokemon_KBase = pickle.load(open('Pokemon_KnowledgeBase.p', 'rb'))
    else:
        print('Please run GenKnowledgeBase.py first to generate the knowledge base.')
        exit(0)
    pokemon_names = pokemon_KBase.keys()
    starters = [['Charmander', 'Squirtle', 'Bulbasaur'], ['Charmeleon', 'Wartortle', 'Ivysaur'],
                ['Charizard', 'Blastoise', 'Venusaur']]
    users = {}
    if os.path.isfile('Users.p'):
        users = pickle.load(open('Users.p', 'rb'))
    print("Professor_Oak : Well hello there young trainer! I see you\'re here for your starter.")
    print("Professor_Oak : What is your name?")
    username = input('Name:').strip()
    user_data = []
    newUser = True
    if username in users.keys():
        newUser = False
        user_data = users[username]
        # user_data -> [starter, evolution, questions asked]
        # at 5 questions,evolution, at 10 after that, second evolution
    user_query = ''
    if not newUser:
        print("Professor_Oak : Welcome back " + username + "!")
        print("Professor_Oak : I see that your " + starters[user_data[1]][user_data[0]] + ' is looking healthy!')
        if user_data[1] < 2:
            print(
                'Professor_Oak : I do believe that your ' + starters[user_data[1]][user_data[0]] + ' will evolve after'
                + ' another ' + str((user_data[1] + 1) * 5 - user_data[2]) + ' questions.')
        else:
            print('Professor_Oak : I must say, I\'m quite impressed that you\'ve asked as many as ' +
                  str(user_data[2] + 15) + ' questions!')
            print('Professor_Oak : You are quite the diligent trainer. ')
            print('Professor_Oak : I can see that you and your ' + starters[user_data[1]][user_data[0]]
                  + ' have come a long way since you first came to my research lab.')
    else:
        print("Professor_Oak : Hello " + username + ". Please select your Gen 1 starter Pokemon.")
        user_query = input()
        while user_query not in starters[0]:
            print("Professor_Oak : Please enter Charmander, Squirtle, or Bulbasaur.")
            user_query = input()
        user_data.append(starters[0].index(user_query))
        user_data.append(0)
        user_data.append(0)
        print('Professor_Oak : I see that you have selected ' + starters[user_data[1]][user_data[0]] +
              '.')
        print('Professor_Oak : ' + pokemon_KBase[starters[user_data[1]][user_data[0]]][0])
        print('Professor_Oak : ' + starters[user_data[1]][user_data[0]] + ' will evolve after 5 questions, then evolve '
                                                                          'again 10 questions after that.')
    print('Professor_Oak : Now then, young trainer. What question do you have about Gen 1 Pokemon for me today?')
    more_Questions = True
    while more_Questions:
        user_query = input()
        user_query = user_query.lower()
        question_asked = False
        if 'bye' not in user_query:
            if 'thank' not in user_query:
                print('Professor_Oak : ' + str(generate_response(user_query, pokemon_names, pokemon_KBase)))
                question_asked = True
            else:
                more_Questions = False
                print("Professor_Oak : You're most welcome young trainer. I wish you many wonderful adventures!")
        else:
            more_Questions = False
            print("Professor_Oak : Farewell young trainer. I wish you many wonderful adventures!")
        if question_asked:
            user_data[2] += 1
            if user_data[1] < 2 and (user_data[1] + 1) * 5 == user_data[2]:
                print('Professor_Oak : Well done ' + username + '! Your ' + starters[user_data[1]][user_data[0]] +
                      ' has evolved into a ' + starters[user_data[1] + 1][user_data[0]] + '!')
                user_data[1] += 1
                user_data[2] = 0
                if user_data[1] < 2:
                    print('Professor_Oak : Don\'t rest on your laurels just yet young trainer! 10 more questions, and'
                          + ' your ' + starters[user_data[1]][user_data[0]] + ' will evolve once more!')
    users[username] = user_data
    pickle.dump(users, open('Users.p', 'wb'))
