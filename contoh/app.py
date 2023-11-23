from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proses_upload', methods=['POST'])
def proses_upload():
    file = request.files['file']

    if file:
        # Simpan file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Baca file yang diunggah
        df = pd.read_excel(file_path)

        # Drop NaN values
        df = df.dropna()

        # Reset index
        df = df.reset_index()

        # Label encoding
        le = LabelEncoder()
        df["pendidikan"] = le.fit_transform(df['pendidikan'])
        df["jenis_kelamin"] = le.fit_transform(df['jenis_kelamin'])

        # Persiapan data
        x = df.drop(["penerimaan"], axis=1)
        y = df["penerimaan"]

        # Training Naive Bayes
        nbc = GaussianNB()
        data_training = nbc.fit(x, y)

        # Prediksi
        y_predict = data_training.predict(x)

        # Data Testing
        pendidikan = 2  # Bachelor's
        jenis_kelamin = 0  # Male
        umur = 35
        masa_kerja = 8
        penghargaan = 0
        penerimaan = np.average([pendidikan, jenis_kelamin, umur, masa_kerja, penghargaan])
        Data_Testing = [[pendidikan, jenis_kelamin, umur, masa_kerja, penghargaan, penerimaan]]

        y_pred = data_training.predict(Data_Testing)
        if y_pred == 1:
            hasil = "Ya"
        elif y_pred == 0:
            hasil = "Tidak"
        else:
            hasil = "error"

        # Menangani hasil "error"
        result = {"result": hasil}
        if hasil == "error":
            return jsonify(result), 500  # 500 adalah kode status untuk kesalahan server
        else:
            # Menampilkan hasil prediksi
            print("Hasil prediksi penerimaan pada karyawan:")
            print(y_predict)

            # Menampilkan hasil klasifikasi
            print("Hasil penerimaan pada karyawan =", hasil)

            from sklearn.metrics import accuracy_score
            print("Nilai Akurasi = %0.2f" % accuracy_score(y, y_predict))

            from sklearn.metrics import classification_report
            print("Laporan Klasifikasi:\n", classification_report(y, y_predict))

            # Diasumsikan 'hasil' adalah hasil klasifikasi
            result = {"result": hasil}

            return jsonify(result)
    else:
        return jsonify({"error": "Tidak ada file yang diberikan"})

@app.route('/hasil')
def hasil():
    result = request.args.get('result', '')
    return render_template('hasil.html', result=result)

if __name__ == '__main__':
    # Pastikan direktori 'uploads' ada
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=False)

