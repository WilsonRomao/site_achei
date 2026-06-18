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
from flasgger import Swagger

ALLOWED_EXTENSIONS = {'xls','xlsx'}
app.config["JWT_SECRET_KEY"] = "super-secret-key-site-achei"
jwt = JWTManager(app)

db = SQLAlchemy(app)

# Configuração do Swagger com suporte a JWT
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Formato: Bearer <seu_token_jwt>"
        }
    },
    "security": [{"Bearer": []}]
}

swagger = Swagger(app, config=swagger_config)
