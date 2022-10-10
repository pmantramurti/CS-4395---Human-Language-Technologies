import pickle
import re
from urllib.request import Request

from bs4 import BeautifulSoup
import requests
from urllib import request
import nltk
from nltk.corpus import stopwords


def web_crawler():
    starter_url = "https://en.wikipedia.org/wiki/Pok%C3%A9mon"

    r = requests.get(starter_url)

    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    url_list = []
    counter = 0
    # write urls to a file
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if link.get('href') not in url_list and 'pokemon' in link_str and '.jpg' not in link_str and \
                'pokemon.co' not in link_str and 'dictionary' not in link_str and 'music' not in \
                link_str and 'archive' not in link_str and 'dexerto' not in link_str and 'aramajapan' \
                not in link_str and 'gematsu' not in link_str and 'tcg' not in link_str and 'faqs' not in\
                link_str and 'usaopoly' not in link_str and 'popmatters' not in link_str and 'twitter' \
                not in link_str and 'auburnpub' not in link_str and 'wpxi' not in link_str and 'support' \
                not in link_str and 'similar.html?' not in link_str and 'siliconera' not in link_str\
                and 'subredditstats' not in link_str and 'mashable' not in link_str:
            url_list.append(link.get('href'))
            counter += 1
        if counter > 40:
            break
    return url_list


def web_scraper(urls):
    counter = 0
    for url in urls:
        file = 'url' + str(counter) + '.txt'
        html = request.urlopen(url).read().decode('utf8')
        souper = BeautifulSoup(html, features="html.parser")
        for script in souper(["script", "style"]):
            script.extract()
        text = souper.get_text()
        text = "".join([chunk for chunk in text.splitlines() if not re.match(r'^\s*$', chunk)])
        with open(file, "w", encoding="utf-8") as f:
            f.write(text)
        counter += 1


def clean_text():
    for i in range(0, 31):
        with open('url' + str(i) + '.txt', "r", encoding="utf-8") as f:
            text = str(f.read())
        text = "".join([t if t != '\n' and t != '\t' and t != ' ' else ' ' for t in text])
        sentences = nltk.sent_tokenize(text)
        for j in range(1, len(sentences)):
            sentences[j] = sentences[j].strip(' ')
        with open('cleantext' + str(i) + '.txt', "w", encoding="utf-8") as f:
            for j in range(1, len(sentences)):
                f.write(sentences[j] + ' ')

def imp_words():
    all_text = ''
    token_dict = {}
    for i in range(0, 31):
        with open('cleantext' + str(i) + '.txt', "r", encoding="utf-8") as f:
            all_text += str(f.read())
    tokens = nltk.word_tokenize(all_text)
    sent_out = nltk.sent_tokenize(all_text)
    tokens = [t.lower() for t in tokens if t.isalpha() and t.lower() not in stopwords.words('english')]
    for token in tokens:
        if token in token_dict:
            token_dict[token] += 1
        else:
            token_dict[token] = 1
    top_tokens = sorted(token_dict.items(), key=lambda x: x[1], reverse=True)[:50]
    print(top_tokens)
    return sent_out
# Top words selected : Pokemon

if __name__ == '__main__':
    poke_urls = web_crawler()
    web_scraper(poke_urls)
    clean_text()# UNCOMMENT THESE ON SUBMISSION
    sent_tokens = imp_words()
    Important_words = ['pokemon', 'game', 'anime', 'region', 'players', 'nintendo', 'go', 'series', 'world', 'plus']
    knowledge_base = {}
    for word in Important_words:
        knowledge_base[word] = []
    for sent in sent_tokens:
        sent_loop = sent.split()
        for word in sent_loop:
            if word.lower() in knowledge_base:
                if sent not in knowledge_base[word.lower()]:
                    knowledge_base[word.lower()].append(sent)
    print(knowledge_base)
    pickle.dump(knowledge_base, open('knowBase.p', 'wb'))
