from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from gensim.utils import tokenize
import scrapy

def plot_2d_graph(vocabs, xs, ys):
    plt.figure(figsize=(8,6))
    plt.scatter(xs, ys, marker = 'o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))

def preprocessing(sentense):
    s = list(tokenize(sentense))
    return s

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

# get urls
start_urls = 'https://www.medicalnewstoday.com/coronavirus'
res = requests.get(start_urls)
soup = BeautifulSoup(res.content, "html.parser")
articles = soup.find_all('a', href=True)
sentence = []

url_list = [
    'https://www.medicalnewstoday.com/articles/coronavirus-vs-flu',
    'https://www.medicalnewstoday.com/articles/covid-19-symptoms',
    'https://www.medicalnewstoday.com/articles/covid-19',
    'https://www.medicalnewstoday.com/articles/early-flu-symptoms',
    'https://www.medicalnewstoday.com/articles/migraine-and-covid-19',
    'https://www.medicalnewstoday.com/articles/what-factors-did-people-who-died-with-covid-19-have-in-common',
    'https://www.medicalnewstoday.com/articles/covid-19-asthma',
    'https://www.medicalnewstoday.com/articles/coronavirus-effects-on-body',
    'https://www.medicalnewstoday.com/articles/coronavirus-prevention',
    'https://www.medicalnewstoday.com/articles/coronavirus-81-of-cases-are-mild-study-says',
    'https://www.medicalnewstoday.com/articles/covid-19-digestive-symptoms-are-common',
    'https://www.medicalnewstoday.com/articles/sex-differences-in-covid-19',
    'https://www.medicalnewstoday.com/articles/covid-19-interview-with-infectious-disease-expert-professor-paul-kellam-part-1',
    'https://www.medicalnewstoday.com/articles/common-coronaviruses-appear-to-be-highly-seasonal',
    'https://www.medicalnewstoday.com/articles/coronavirus-myths-explored',
    'https://www.medicalnewstoday.com/articles/256521',
    'https://www.medicalnewstoday.com/articles/166606',
    'https://www.medicalnewstoday.com/articles/15107',

    'https://www.medicalnewstoday.com/articles/new-study-pinpoints-loss-of-smell-and-taste-as-covid-19-symptoms#Early-signs-of-COVID-19?',

]
for url in url_list:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    contents = soup.find(attrs={'class': 'article-body'})
    paragraphs = contents.findAll('p')
    for p in paragraphs:
        txt = p.text
        sent = sent_tokenize(txt)
        for s in sent:
            w = word_tokenize(s)
            w = [word.lower() for word in w if word.isalpha()]
            sentence.append(w)
    lists = contents.findAll('li')
    for p in lists:
        txt = p.text
        sent = sent_tokenize(txt)
        for s in sent:
            w = word_tokenize(s)
            w = [word.lower() for word in w if word.isalpha()]
            sentence.append(w)

model = Word2Vec(sentence, size=300, window=3, min_count=1, workers=1)

word_vectors = model.wv

vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

print(word_vectors.similarity(w1='disease', w2='hand'))

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
xys = pca.fit_transform(word_vectors_list)
xs = xys[:, 0]
ys = xys[:, 1]

plot_2d_graph(vocabs, xs, ys)
plt.show()