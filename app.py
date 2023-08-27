from flask import Flask
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# app.secret_key = 'MySecretKey' ----> utilised here learned by fynd9

from routes import *

if __name__ == '__main__':
    app.run(debug=True)


