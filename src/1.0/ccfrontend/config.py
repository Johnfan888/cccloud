#-*- coding:utf-8  -*-
'''
import os
CSRF_ENABLED = True
SECRET_KEY = '123456'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CSRF_ENABLED = True
SECRET_KEY = '123456'
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root:1234qwer@localhost/VM_manager'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
db = SQLAlchemy(app)