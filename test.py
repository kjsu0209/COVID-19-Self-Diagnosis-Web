import pandas as pd
from textblob import TextBlob

FILEURL = 'dataset-1.csv'

word_block = {}  #Word block

def symptom_counter(symptoms, s):
    # symptom already exists in the dictionary variable
    if s in symptoms.keys():
        symptoms[s] += 1
    else:
        symptoms[s] = 1

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import brown


def word_classify(word, value):  # Categorizing Words
    lemmatizer = WordNetLemmatizer()
    porter = PorterStemmer()
    keyword = value

    if word == 'VBG' or word == 'VBN' or word == 'VBD':
        keyword = porter.stem(value)
    elif word == 'NNS':
        keyword = lemmatizer.lemmatize(value)
    return keyword


def add_word(key, word):  # Add a word to the word dictionary
    if key in word_block.keys():
        word_block[key].append(word)
    else:
        word_block[key] = [word]


def produce_morph(s):
    words = word_tokenize(s)

    tag_block = nltk.pos_tag(words)
    # print(tag_block)
    if len(tag_block) == 1:  # 단일어
        keyword = word_classify(tag_block[0][1], tag_block[0][0])
    else:  # 복합어
        index = len(tag_block)
        # 전치사가 있는 경우
        preposition = None
        for i in range(index):
            if 'IN' in tag_block[i]:
                preposition = tag_block[i][0]
        if preposition == 'with':
            keyword = word_classify(tag_block[0][1], tag_block[0][0])
        else:
            keyword = word_classify(tag_block[index - 1][1], tag_block[index - 1][0])

    add_word(keyword, s)

    return keyword

def preprocess(symptoms, df):
    num = 0
    for i, row in df.iterrows():
        # check symptom data exists in the row
        if row['symptom']:
            val = row['symptom']
            # Word not found
            if val != val:
                continue
            num += 1  # count the number of cases
            if ', ' in val:
                for s in val.split(', '):
                    s = produce_morph(s)
                    symptom_counter(symptoms, s)
            else:
                val = produce_morph(val)
                symptom_counter(symptoms, val)

    return num


# initiate file
def init_text():
    symptoms = {}

    # read csv file
    df = pd.read_csv(FILEURL)
    preprocess(symptoms, df)

    return symptoms


# return a word block of key symptom
def get_word_block(keyword):
    return word_block[keyword]


def get_rad_value(keyword):
    symptoms = {}
    if len(keyword) == 0:
        return 0

    words = word_tokenize(keyword)
    tag_block = nltk.pos_tag(words)
    if len(tag_block) == 1:  # 단일어
        word = word_classify(tag_block[0][1], tag_block[0][0])
    else:
        word = keyword
    # read csv file
    df = pd.read_csv(FILEURL)
    case_num = preprocess(symptoms, df)

    if word in symptoms.keys():
        return symptoms[word]/case_num
    else:
        return 0


# main function to print results
def main():
    symptoms = {}

    # read csv file
    df = pd.read_csv(FILEURL)
    case_num = preprocess(symptoms, df)

    # print values
    print('case num : ', case_num)
    print("{0:25}{1:20}{2:20}".format("symptom_name", "count", "RAD value"))
    for s, n in symptoms.items():
        print("{0:25}{1:20}{2:20}".format(s, str(n), (n/case_num)))


if __name__ == '__main__':
    main()