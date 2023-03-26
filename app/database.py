from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

db.init_app(app)