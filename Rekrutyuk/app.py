from crypt import methods
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/Prediction', methods=['GET','POST'])
def prediksi():
    return render_template("prediksi.html")



if __name__ == "__main__":
    app.run(debug=True)