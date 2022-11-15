import urllib

import nltk
import bs4 as bs
import requests
import re
import pickle
from urllib import request


def web_crawler():
    starter_url = "https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon"

    r = requests.get(starter_url)

    data = r.text
    soup = bs.BeautifulSoup(data, features="html.parser")
    url_list = []
    count = 0
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if link.get('href') not in url_list and 'type' not in link_str and '#' not in link_str \
                and 'Pok%C3%A9mon' not in link_str and 'Category' not in link_str and 'Special' not in \
                link_str and 'User' not in link_str and 'www' not in link_str and \
                link_str.startswith('/wiki/') and 'Pok%C3%A9' not in link_str and 'Species' not in \
                link_str and 'Party' not in link_str and 'Types' not in link_str and 'Generation' not \
                in link_str and 'Unown_Report' not in link_str and 'Local_Sitemap' not in link_str:
            url_list.append(link.get('href'))
            count += 1
        if count == 151:
            break
    poke = []
    for url in url_list:
        poke.append(url.split('/')[2])
    return poke


def web_scraper(pokemon_names):
    counter = 0
    for name in pokemon_names:
        counter += 1
        print(counter)
        file = name + '.txt'
        html = request.urlopen('https://pokemon.fandom.com/wiki/' + name).read().decode('utf8')
        article_html = bs.BeautifulSoup(html, features="html.parser")
        article_paragraphs = article_html.find_all('p')
        article_text = ''
        for para in article_paragraphs:
            article_text += para.text
        user_agent = 'Mozilla/5.0'
        headers = {'User-Agent': user_agent}
        request1 = urllib.request.Request(url=('https://bulbapedia.bulbagarden.net/wiki/' + name), headers=headers)
        html = urllib.request.urlopen(request1).read().decode('utf8')
        article_html = bs.BeautifulSoup(html, features="html.parser")
        article_paragraphs = article_html.find_all('p')
        for para in article_paragraphs:
            article_text += para.text
        article_text = re.sub(r'\[\d*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        textArray = article_text.split()
        article_text = ' '.join(textArray[28:])
        textArray = article_text.split('.ogg')
        article_text = textArray[-1]
        with open(file, "w", encoding="utf-8") as f:
            f.write(article_text)


def clean_text(pokemon_names):
    for name in pokemon_names:
        with open(name + '.txt', "r", encoding="utf-8") as f:
            text = str(f.read())
        text = "".join([t if t != '\n' and t != '\t' and t != ' ' else ' ' for t in text])
        text = text.replace(".",". ")
        temp_sent = nltk.sent_tokenize(text)
        sentences = []
        for sent in temp_sent:
            if sent not in sentences:
                sentences.append(sent)
        for j in range(1, len(sentences)):
            sentences[j] = sentences[j].strip(' ')
        with open('cleantext_' + name + '.txt', "w", encoding="utf-8") as f:
            for j in range(0, len(sentences)):
                f.write(sentences[j] + ' ')


def genKnowledgeBase(pokem_names):
    diction = {}
    for name in pokem_names:
        with open('cleantext_' + name + '.txt', "r", encoding="utf-8") as f:
            text = str(f.read())
        poke_sent = nltk.sent_tokenize(text)
        diction[name] = poke_sent
    return diction


if __name__ == '__main__':
    poke_names = web_crawler()
    web_scraper(poke_names)   # Uncomment these to run the full knowledge base generator form scratch
    clean_text(poke_names)
    Pokemon_KnowledgeBase = genKnowledgeBase(poke_names)
    counter = 0
    while counter < 151:
        counter = 0
        for pokemon in Pokemon_KnowledgeBase.keys():
            HasLine = False
            if 'is a' in Pokemon_KnowledgeBase[pokemon][0]:
                HasLine = True
                counter += 1
            if not HasLine:
                del Pokemon_KnowledgeBase[pokemon][0]
    for pokemon in Pokemon_KnowledgeBase.keys():
        lineToFix = Pokemon_KnowledgeBase[pokemon][0]
        lineToFix = lineToFix.replace('(s)', '')
        lineToFix = lineToFix.replace('(DW)', '')
        lineToFix = lineToFix.split('(')
        lineToFix = pokemon + ' (' + '('.join(lineToFix[1:])
        Pokemon_KnowledgeBase[pokemon][0] = lineToFix
    pickle.dump(Pokemon_KnowledgeBase, open('Pokemon_KnowledgeBase.p', 'wb'))
