import flask
import flask_login
import sqlite3
import os
import json
import datetime

def databaseFilePath():
    return os.path.join(os.path.dirname(__file__),'../database/project.sqlite3')

def fileStoragePath():
    return os.path.join(os.path.dirname(__file__),'../database/qms')

def getDoc(code):
    files=os.listdir(fileStoragePath())
    try:
        for file in files:
            if file.upper().startswith(code.upper()) and file.lower().endswith('.markdown'):
                fp=open(file=os.path.join(fileStoragePath(),file), mode='r',encoding='utf8')
                content=fp.read()
                fp.close()
                return content
    except Exception as e:
        print(e)
        return None
    return None

