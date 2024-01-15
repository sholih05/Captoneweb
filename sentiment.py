import numpy as np
from flask import Flask, request, render_template
import joblib
import os
import pandas as pd
import pickle
from nltk.tokenize import word_tokenize
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory



model = joblib.load(open(os.path.join(os.path.dirname(__file__), 'model/svm1_model.pkl'), 'rb'))
cv = pickle.load(open(os.path.join(os.path.dirname(__file__), 'model/cobaa.pickle'), 'rb'))

#Filtering Data filter_text: Fungsi untuk membersihkan teks dengan menghapus URL, lanjutan kata, tanda baca, hashtag, dan angka menggunakan ekspresi reguler.
def filter_text(text):
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)  # Remove URLs
    text = re.sub(r'\(cont\)', ' ', text)  # Remove continuations
    text = re.sub(r'[!"”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]', ' ', text)  # Remove punctuation
    text = re.sub(r'#\S+', '', text)  # Remove hashtags
    text = re.sub(r'\d+', ' ', text)  # Remove numbers
    return text

#Stopword Removal  Fungsi untuk menghapus stopwords (kata-kata umum yang sering muncul dan tidak memberikan banyak informasi) dari daftar token.
factory = StopWordRemoverFactory()
stopword_list = factory.get_stop_words()

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stopword_list and len(word) > 3]


#Slang Word Normalization Fungsi untuk menggantikan kata-kata slang dengan versi normalnya menggunakan data kamus slang yang disimpan dalam file CSV.
path_dataslang = open(os.path.join(os.path.dirname(__file__), 'model/kamus.csv'))
dataslang = pd.read_csv(path_dataslang, encoding = 'utf-8', header=None, sep=";")

def replaceSlang(word):
  if word in list(dataslang[0]):
    indexslang = list(dataslang[0]).index(word)
    print(indexslang)
    return dataslang[1][indexslang]
  else:
    return word


#Stemming Fungsi untuk melakukan stemming pada kata-kata (menghapus imbuhan dan membawa kata ke bentuk dasarnya).
factory = StemmerFactory()
ind_stemmer = factory.create_stemmer()
white_list = ["bali"]

def stemmer(line):
  valid = list()
  for word in line:
    if(word not in white_list):
      word = ind_stemmer.stem(word)
    if(len(word)>2):
      valid.append(word)
  return valid

def predict_sentiment(test):
    test = test
    
    data_casefolded = test.lower()
    data_filtered = filter_text(data_casefolded)
    data_tokenized = word_tokenize(data_filtered)
    data_no_stopwords = remove_stopwords(data_tokenized)
    
    replaceslang = replaceSlang(data_no_stopwords)

    data_stemmed = stemmer(replaceslang)
    data_preprocessed = ' '.join(data_stemmed)

    text = [str(data_preprocessed)]
    test_vector = cv.transform(text).toarray()
    pred = model.predict(test_vector)
    return pred[0]



