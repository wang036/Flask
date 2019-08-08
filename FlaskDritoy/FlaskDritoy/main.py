import os
import pymysql
from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_restful import Resource, Api
from sqlalchemy import create_engine


pymysql.install_as_MySQLdb()

app = Flask(__name__)
csrf = CSRFProtect(app)

api = Api(app)


class Hello(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(Hello, '/API')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "Student.sqlite")
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1111@localhost/school"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '123'

models = SQLAlchemy(app)  # 关联sqlalchemy和flask应用
