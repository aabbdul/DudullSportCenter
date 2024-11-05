from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrasi-login')
def register():
    return render_template('registrasi-login/index.html')

if __name__ == '__main__':
    app.run(debug=True)
