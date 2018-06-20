from flask import Flask

app = Flask(__name__)
from app import main

#session makes it possible to save variables and use within other functions
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.secret_key = 'asldkje223423ssdj*&#sdh!@#Lj'
