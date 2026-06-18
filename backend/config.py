# configuração geral da aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#__________INITIALISATIONS____________________
app = Flask(__name__)
CORS(app)


import os

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///appdatebase.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


from flask_jwt_extended import JWTManager

ALLOWED_EXTENSIONS = {'xls','xlsx'}
app.config["JWT_SECRET_KEY"] = "super-secret-key-site-achei"
jwt = JWTManager(app)

db = SQLAlchemy(app)
