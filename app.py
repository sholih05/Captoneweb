# Import library Flask untuk membuat web application
from flask import Flask, flash, render_template, request, jsonify,send_file
# Import library Keras untuk model machine learning
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import pandas as pd
from sklearn import preprocessing
# Import library TensorFlow untuk machine learning
import tensorflow as tf
from tensorflow import keras
from skimage import transform, io
import numpy as np
import os
from PIL import Image
from datetime import datetime
from keras.preprocessing import image
from flask_cors import CORS
# Import library Natural Language Toolkit (nltk) untuk pemrosesan bahasa alami
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import json
import random


from flask import Flask, redirect,render_template,request
from flask import url_for
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pytz 
from datetime import datetime

from model_chatbot import chatbot_response, getResponse, predict_class
#Sentiment Analysis
from sentiment import predict_sentiment
# Time Format
target_timezone = 'Asia/Jakarta'
import mysql.connector
import pymysql
# Inisialisasi aplikasi Flask
app = Flask(__name__)






# Memuat model machine learning untuk klasifikasi gambar
modelxception = load_model("model/Xception.h5")




# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'review 1',
}
app.secret_key = 'bebasapasaja'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='si_sawi1'




mysql = MySQL(app)
# Mengonfigurasi folder untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', 'jfif'}

# Memuat model chatbot dan data terkait ini untuk api chatbot
model = load_model('model/models.h5')
intents = json.loads(open('model/data.json').read())
words = pickle.load(open('model/texts.pkl', 'rb'))
classes = pickle.load(open('model/labels.pkl', 'rb'))


# Fungsi untuk memeriksa jenis file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_detection_history_to_mysql(username, prediction, confidence):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Pastikan tabel history_detection ada, jika tidak, buat tabel
            sql_create_table = """
                CREATE TABLE IF NOT EXISTS history_detection (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    username VARCHAR(255) NOT NULL,
                    prediction VARCHAR(255) NOT NULL,
                    confidence FLOAT NOT NULL
                )
            """
            cursor.execute(sql_create_table)

            # Masukkan data deteksi ke dalam tabel history_detection
            sql_insert = """
                INSERT INTO history_detection (username, prediction, confidence)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql_insert, (username, prediction, confidence))

        connection.commit()
        print("Detection history inserted successfully!")
    except Exception as e:
        print(f"Error inserting detection history: {e}")
    finally:
        connection.close()




# Enable CORS for all routes
#Ini mengizinkan akses lintas domain, terutama untuk metode POST dan OPTIONS, sehingga memungkinkan formulir dari domain lain untuk berinteraksi dengan aplikasi secara aman dan terkendali.
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors_headers)

def get_user_info_from_database(username):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Sesuaikan query berdasarkan struktur tabel pengguna Anda
            sql = "SELECT * FROM tb_users WHERE username=%s"
            cursor.execute(sql, (username,))
            user_info = cursor.fetchone()
        return user_info
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()



# Rute dan Tampilan
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re_password']
        level = request.form['level']

        #cek username atau email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE username=%s OR email=%s',(username, email, ))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO tb_users VALUES (NULL, %s, %s, %s, %s, %s)', (username, email, password, re_password, level))
            mysql.connection.commit()
            flash('Registrasi Berhasil','success')
        else :
            flash('Username atau email sudah ada','danger')
    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #cek data username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_users WHERE username=%s',(username, ))
        akun = cursor.fetchone()
        if akun is None:
            flash('Login Gagal, Cek Username Anda','danger')
        elif not (akun[3], password):
            flash('Login gagal, Cek Password Anda', 'danger')
        else:
            session['loggedin'] = True
            session['username'] = akun[1]
            session['password'] = akun[3]
            session['level'] = akun[5]
            return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    #menghapus sesi pengguna
    return redirect(url_for('login'))




@app.route("/", methods=['GET', 'POST'])
def main():
    if 'loggedin' in session:
        # user_info = get_user_info_from_database(username)
        return render_template('index.html', username=session['username'],)
    flash('Harap Login dulu','danger')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/classification", methods=['GET', 'POST'])
def classification():
    return render_template("classifications.html")

# Rute untuk memproses pengiriman file gambar dan melakukan prediksi
@app.route('/submit', methods=['POST'])
def predict():
    if 'file' not in request.files:
        resp = jsonify({'message': 'Tidak ada gambar dalam permintaan'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')
    filename = "temp_image.png"
    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors["message"] = 'Jenis file {} tidak diizinkan'.format(file.filename)

    if not success:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Mengonversi gambar ke mode RGB
    img = Image.open(img_url).convert('RGB')
    now = datetime.now()
    predict_image_path = 'static/uploads/' + now.strftime("%d%m%y-%H%M%S") + ".png"
    image_predict = predict_image_path
    img.convert('RGB').save(image_predict, format="png")
    img.close()

    # Menyiapkan gambar untuk prediksi
    img = image.load_img(predict_image_path, target_size=(128, 128, 3))
    x = image.img_to_array(img)
    x = x / 127.5 - 1
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    # Melakukan prediksi dengan model
    prediction_array_xception = modelxception.predict(images)
    
    # Menyiapkan respons API
    class_names = ['Sawi Sehat', 'Ulat Grayak (Spodoptera litura)', 'Ulat Tanah (Agrotis sp)', 'Ulat Tritip (Plutella xylostella)']

    result = {
        # "filename": predict_image_path,
        "prediction": class_names[np.argmax(prediction_array_xception)],
        "confidence": '{:2.0f}%'.format(100 * np.max(prediction_array_xception))
        
        
    }

    # Menyimpan deteksi ke dalam tabel history_detection
    insert_detection_history_to_mysql(session.get('username'), result["prediction"], np.max(prediction_array_xception))
    

    # Merender template dan menampilkan hasil prediksi dan kelas yang diprediksi
    return render_template("classifications.html", img_path=predict_image_path,
                           predictionxception=class_names[np.argmax(prediction_array_xception)])
#Mengambil indeks kelas dengan nilai probabilitas tertinggi pada model

# Rute untuk tampilan chatbot
@app.route("/chatbot", methods=['GET', 'POST'])
def chatbot():
    return render_template("chatbot.html")



# Rute endpoint API untuk interaksi dengan chatbot
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


#rute untuk chatbot api ke mobile
@app.route('/chat', methods=["GET", "POST"])
def chatSawiBot():
    chatInput = request.get_json().get('chatInput')
    ints = predict_class(chatInput, model)
    return jsonify(botReply=getResponse(ints, intents))

@app.route('/api', methods=['POST'])
def prediksikeflutter():
    if 'file' not in request.files:
        resp = jsonify({'message': 'Tidak ada gambar dalam permintaan'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')
    filename = "temp_image.png"
    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors["message"] = 'Jenis file {} tidak diizinkan'.format(file.filename)

    if not success:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Mengonversi gambar ke mode RGB
    img = Image.open(img_url).convert('RGB')
    now = datetime.now()
    predict_image_path = 'static/uploads/' + now.strftime("%d%m%y-%H%M%S") + ".png"
    image_predict = predict_image_path
    img.convert('RGB').save(image_predict, format="png")
    img.close()

    # Menyiapkan gambar untuk prediksi
    img = image.load_img(predict_image_path, target_size=(128, 128, 3))
    x = image.img_to_array(img)
    x = x / 127.5 - 1
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    # Melakukan prediksi dengan model
    prediction_array_xception = modelxception.predict(images)
    
    # Menyiapkan respons API
    class_names = ['Sawi Sehat', 'Ulat Grayak (Spodoptera litura)', 'Ulat Tanah (Agrotis sp)', 'Ulat Tritip (Plutella xylostella)']

    result = {
        # "filename": predict_image_path,
        "prediction": class_names[np.argmax(prediction_array_xception)],
        "confidence": '{:2.0f}%'.format(100 * np.max(prediction_array_xception))
        
        
    }
     # Mengembalikan respons dalam format JSON
    return jsonify(result)



@app.route('/history/<int:page>')
def get_history(page):
    entries_per_page = 50

    try:
        total_entries = detection_history.query.count()
        start_index = (page - 1) * entries_per_page
        end_index = start_index + entries_per_page

        paginated_history = detection_history.query.slice(start_index, end_index).all()

        result = []
        for entry in paginated_history:
            result.append({
                "id": entry.id,
                "tanggal": entry.tanggal,
                "username": entry.username,
                "prediction": entry.prediction,
                "confidence": entry.confidence
            })

        return jsonify({"history_list": result, "total_entries": total_entries})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Error fetching data"}), 500


@app.route('/history')
def detection_history():
    try:
        page = request.args.get('page', 1, type=int)
        entries_per_page = 50
        start_index = (page - 1) * entries_per_page
        end_index = start_index + entries_per_page

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Ubah query untuk mengambil hanya kolom yang diperlukan
            sql = f"SELECT id, tanggal, username, prediction, confidence FROM history_detection LIMIT {start_index}, {entries_per_page}"
            cursor.execute(sql)
            history_data = cursor.fetchall()
            print("History Data:", history_data)

            # Mengonversi hasil fetch ke dalam format yang sesuai
            history_list = []
            for entry in history_data:
                history_list.append({
                    'id': entry[0],
                    'tanggal': entry[1],
                    'username': entry[2],
                    'prediction': entry[3],
                    'confidence': entry[4]
                })
    except Exception as e:
        print(f"Error fetching data: {e}")
        history_list = []  # Atur history_list ke daftar kosong jika terjadi kesalahan
    finally:
        connection.close()

    return render_template('history.html', history_list=history_list)




# Fungsi untuk membuat koneksi MySQL
def create_connection():
    return pymysql.connect(host='127.0.0.1', user='root', password='', database='review 1')

# ...

# Rute endpoint /layanan
@app.route("/layanan", methods=['GET', 'POST'])
def layanan():
    # Inisialisasi variabel
    title = "sisawi | Layanan"
    view = "layanan"
    predict = 0  # Inisialisasi nilai predict dengan 0 memeriksa apakah analisis sentimen telah dilakukan atau belum.

    # Mendapatkan data sentiment dari database
    sentiment = fetch_sentiment()
   
    # Memproses permintaan POST
    if request.method == 'POST':
        word = request.form['review']  # Mengambil data review dari formulir POST
        predict = predict_sentiment(word)  # Melakukan prediksi sentimen berdasarkan review

        # Mendapatkan waktu lokal
        utc_time = datetime.utcnow()
        local_timezone = pytz.timezone(target_timezone)
        local_time = pytz.utc.localize(utc_time).astimezone(local_timezone)

        # Membuat koneksi ke database
        connection = create_connection()
        try:
            with connection.cursor() as cursor:
                # Memasukkan data review ke database
                sql_insert_review = """
                    INSERT INTO Review (review, score, date)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_insert_review, (word, int(predict), local_time.replace(microsecond=0)))
                connection.commit()

                # Mengambil 5 review terbaru dari database
                sql_fetch_reviews = """
                    SELECT * FROM Review ORDER BY date DESC LIMIT 5
                """
                cursor.execute(sql_fetch_reviews)
                getReview = cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error: {e}")
            getReview = []
        finally:
            # Menutup koneksi ke database
            connection.close()

        # Merender template "layanan.html" dengan hasil prediksi,  data sentiment
        return render_template("layanan.html", predict=predict, active=view, title=title, sentiment=sentiment)

    # Memproses permintaan GET
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Mengambil 5 review terbaru dari database
            sql_fetch_reviews = """
                SELECT * FROM Review ORDER BY date DESC LIMIT 5
            """
            cursor.execute(sql_fetch_reviews)
            getReview = cursor.fetchall()
    except pymysql.Error as e:
        print(f"Error: {e}")
        getReview = []
    finally:
        # Menutup koneksi ke database
        connection.close()

    # Merender template "layanan.html" dengan hasil prediksi, dan data sentiment
    return render_template("layanan.html", active=view, title=title, predict=predict, sentiment=sentiment)

# digunakan untuk mengambil data sentimen dari tabel Review dalam database
def fetch_sentiment():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql_fetch_sentiment = """
                SELECT score, COUNT(score) FROM Review GROUP BY score
            """
            cursor.execute(sql_fetch_sentiment)
            sentiment = cursor.fetchall()
            return sentiment
    except pymysql.Error as e:
        print(f"Error fetching sentiment: {e}")
        return []
    finally:
        connection.close()

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
