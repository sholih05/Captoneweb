
import random
import json
import pickle
import numpy as np
import nltk


from nltk.stem import WordNetLemmatizer
from keras.models import load_model

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()



# Memuat model chatbot dan data terkait
model = load_model('model/models.h5')
intents = json.loads(open('model/data.json').read())
words = pickle.load(open('model/texts.pkl', 'rb'))
classes = pickle.load(open('model/labels.pkl', 'rb'))

#preprocessing  tokenisasi dan lemmatisasi
# Fungsi untuk membersihkan kalimat input
def clean_up_sentence(sentence):
    # Tokenisasi pola kata menjadi array
    #proses memecah sebuah teks atau kalimat menjadi unit-unit yang lebih keci
    sentence_words = nltk.word_tokenize(sentence)
    # Memberi kata yang lebih pendek untuk setiap kata
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Fungsi untuk menghasilkan array bag of words: 0 atau 1 untuk setiap kata yang ada dalam kalimat sebagai input untuk model machine learning.
def bow(sentence, words, show_details=True):
    # Tokenisasi pola
    sentence_words = clean_up_sentence(sentence)
    # Bag of words - matriks N kata, matriks kosakata
    bag = [0] * len(words)
    #Inisialisasi ini bertujuan untuk membuat vektor bag-of-words yang akan digunakan untuk merepresentasikan keberadaan atau ketiadaan kata-kata dalam kalimat.
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # Memberikan nilai 1 jika kata saat ini ada dalam posisi kosakata
                bag[i] = 1
                if show_details:
                    print("ditemukan dalam tas: %s" % w)

    return np.array(bag)

# Fungsi untuk memprediksi kelas chatbot berdasarkan input
def predict_class(sentence, model):
    #fungsi ini memproses kalimat input, menggunakan model deep learning untuk memprediksi kelasnya, dan mengembalikan informasi tentang intent dan probabilitasnya
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    #untuk mendapatkan hasil prediksi dalam bentuk probabilitas untuk setiap kelas.
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Diurutkan berdasarkan kekuatan probabilitas
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

    return return_list

# Fungsi untuk mendapatkan respons dari data intents berdasarkan hasil prediksi
def getResponse(ints, intents_json):
    if ints and len(ints) > 0:
        tag = ints[0].get('intent')
        list_of_intents = intents_json.get('intents', [])

        for i in list_of_intents:
            if i.get('tag') == tag:
                result = random.choice(i.get('responses', []))
                return result

    return "Maaf, saya tidak mengerti pertanyaan Anda."


# Fungsi untuk memberikan respons chatbot berdasarkan input pengguna
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


