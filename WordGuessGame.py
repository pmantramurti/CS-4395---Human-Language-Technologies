import nltk
import sys
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')


def procTok(tokens_in):
    tokens_proc = [t for t in tokens_in if t.isalpha() and
                   t not in stopwords.words('english') and len(t) > 5]
    lemma = WordNetLemmatizer()
    tokens_out = [lemma.lemmatize(t) for t in set(tokens_proc)]
    tags = nltk.pos_tag(tokens_out)
    print('First 20 tagged items : ')
    print(tags[0:20])
    nouns = []
    for token, pos in tags:
        if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS':
            nouns.append(token)
    return tokens_proc, nouns


def make_bank():
    if len(sys.argv) != 2:
        print("No file name found. Please run again with file name.")
        exit()
    file = open(sys.argv[1], 'r')
    raw_text = file.read()
    tokens = nltk.word_tokenize(raw_text)
    text = nltk.Text(tokens)
    text_tokens = [t.lower() for t in text]
    text_unique_tokens = set(text_tokens)
    lex_div = len(text_unique_tokens) / len(text_tokens)
    print("The Lexical Diversity is: " + str(round(lex_div, 2)))
    proc_tokens, noun_list = procTok(text_tokens)
    noun_dict = {}
    for token in proc_tokens:
        if token in noun_list and token not in noun_dict:
            noun_dict[token] = 1
        elif token in noun_list:
            noun_dict[token] += 1
    sorted_nouns = sorted(noun_dict.items(), key=lambda x: x[1], reverse=True)
    word_bank = {}
    for j in range(0, 50):
        word_bank[sorted_nouns[j][0]] = sorted_nouns[j][1]
    print('The top 50 most common words are:')
    print(word_bank)
    print()
    return word_bank


if __name__ == '__main__':
    options = list(make_bank().keys())
    score = 5
    while True:
        wordChoice = randint(0, 50)
        answer = ''
        guess = ''
        guesses = []
        for i in list(options[wordChoice]):
            answer += i
        for i in list(answer):
            guess += "_"
        counter = 0
        print("Guess This Word!")
        while True:
            if score < 0:
                print("You have run out of guesses. The answer was " + str(answer) + ". GAME OVER!")
                break
            if guess == answer:
                print("You win! Your score is " + str(score) + ". Congratulations!")
                break
            print(guess)
            ans = input('Your score is ' + str(score) + '. Please enter a guess: ')
            if ans == '!':
                print("Game exited.")
                print("Final Score : " + str(score))
                print("Final Word : " + answer)
                sys.exit(0)
            if ans not in guesses and len(ans) == 1 and ans.isalpha():
                guesses.append(ans)
                guess_list = list(guess)
                for i in range(0, len(answer)):
                    if list(answer)[i] == ans:
                        counter += 1
                        guess_list[i] = ans
                guess = "".join(guess_list)
                if counter == 0:
                    score -= 1
                    print("That was an incorrect guess. Your score is now " + str(score) + ".")
                else:
                    score += 1
                    print("That was a great guess! Your score is now " + str(score) + ".")
                counter = 0
            else:
                print("That was an invalid guess. Try again.")
