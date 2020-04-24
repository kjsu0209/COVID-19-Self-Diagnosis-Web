from flask import (
    Flask, redirect, render_template, request, url_for, jsonify
)
import test
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def main():
    total_cases = 0
    total_deaths = 0

    county = {}
    # url = "https://www.gov.ie/en/press-release/17f5cb-statement-from-the-national-public-health-emergency-team-tuesday-14-/"
    url = "https://www.gov.ie/en/press-release/f4ad12-statement-from-the-national-public-health-emergency-team-thursday-23/"
    res = requests.get(url)

    soup = BeautifulSoup(res.content, "html.parser")
    tables = soup.find_all('table')
    for table in tables:
        if 'Total number of cases' in table.text:   # get total number of cases and death
            tr = table.find_all('tr')
            for row in tr:
                if 'Total number of cases' in row.text:
                    td = row.find_all('td')
                    total_cases = td[1].text
                if 'Total number of deaths' in row.text:
                    td = row.find_all('td')
                    total_deaths = td[1].text
        elif 'Carlow' in table.text:
            tr = table.find_all('tr')
            for row in tr:
                td = row.find_all('td')
                if td[0].text not in county.keys():
                    county[td[0].text] = td[1].text
    c = json.dumps(county)
    return render_template('main.html', total_cases=total_cases, total_deaths=total_deaths, county=c)

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec


@app.route('/step1')    # Get a string of symptom
def step1():
    # Get arguments and initiate variables
    symptom_string = request.args.get('symptom')

    symptoms = []
    symptom = test.init_text()

    # Get Model
    model = Word2Vec.load('word2vec2.model')
    word_vectors = model.wv

    # Word tokenize
    lemmatizer = WordNetLemmatizer()
    porter = PorterStemmer()

    # Get symptoms from text
    sentences = sent_tokenize(symptom_string)
    for sentence in sentences:
        if len(sentence) == 0:
            break

        words = word_tokenize(sentence)
        tag_block = nltk.pos_tag(words)

        for word, tag in tag_block:
            print(word, tag)
            if tag == 'JJ' or tag == 'JJR' or tag == 'RB':
                continue

            if tag == 'NN':  # tag is entity
                for s in symptom.keys():
                    if word == s:
                        symptoms.append(s)
            elif tag == 'VBG' or tag == 'VBP' or tag == 'VBN' or tag == 'VBD':
                keyword = porter.stem(word)
                for s in symptom.keys():  # Check symptom could be happen in COVID-19
                    if keyword == s:
                        symptoms.append(s)
            elif tag == 'NNS':
                keyword = lemmatizer.lemmatize(word)
                for s in symptom.keys():  # Check symptom could be happen in COVID-19
                    if keyword == s:
                        symptoms.append(s)
            elif word in word_vectors.vocab.keys():  # find symptom word based on similarity
                s_symptom = word_vectors.similarity(w1=word, w2='symptom')
                s_difficulty = word_vectors.similarity(w1=word, w2='difficulty')
                if s_symptom > 0.8 and s_difficulty > 0.9:
                    print(word, ' similarity:', s_symptom, ', ', s_difficulty)
                    symptoms.append(word)

    return jsonify(symptoms=symptoms)


@app.route('/step3')    # Get a string of symptom
def step3():
    symptom_string = request.args.get('symptom')
    symptoms = symptom_string.split(',')
    print(symptom_string)

    # The most common symptoms of COVID-19 from https://www.who.int/news-room/q-a-detail/q-a-coronaviruses
    common_list = ['fever', 'tiredness', 'cough', 'ache', 'pain', 'breathing', 'diarrhea']

    result = {}
    count = 0

    for s in symptoms:
        if len(s) == 0:
            break
        rad_value = test.get_rad_value(s)
        if rad_value > 0:
            result[s] = rad_value
            count += 1
        else:
            if s in common_list:
                result[s] = 1  # There is no case with this symptom in RAD, but it is common symptom
            else:
                result[s] = 0  # There is no case with this symptom in RAD

    c = json.dumps(result)

    return jsonify(rad=[c])


if __name__ == '__main__':
    app.run()
