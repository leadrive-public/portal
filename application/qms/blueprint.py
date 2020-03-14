import flask
import flask_login
import sqlite3
import os
import json

from . import service as service

bp = flask.Blueprint('qms', __name__, url_prefix='/qms')

def basePath():
    return os.path.dirname(__file__)

@bp.route('/')
def default():
    user=flask_login.current_user
    if user.is_authenticated:
        return flask.render_template('qms_home.html', user=user)
    else:
        return flask.render_template('qms_home.html')

@bp.route('/manual')
def manual():
    user=flask_login.current_user
    return flask.render_template('qms_manual.html', user=user)

@bp.route('/procedures')
def procedures():
    user=flask_login.current_user
    return flask.render_template('qms_procedures.html', user=user)

@bp.route('/wi-daily')
def workinstructions_daily():
    user=flask_login.current_user
    return flask.render_template('qms_workinstructions_daily.html', user=user)

@bp.route('/wi-eng')
def workinstructions_engineering():
    user=flask_login.current_user
    return flask.render_template('qms_workinstructions_engineering.html', user=user)

@bp.route('/files/<string:file>')
def files(file):
    user=flask_login.current_user
    return flask.render_template('qms_files.html', user=user, file=file)

@bp.route('/files/<string:file>/<string:version>')
def filesWithVersion(file, version):
    user=flask_login.current_user
    return flask.render_template('qms_files.html', user=user, file=file, version=version)

@bp.route('/service', methods=['POST','GET'])
def webService():
    req = flask.request.get_json()
    func = req['function']
    rsp = None
    if func == 'getDoc':
        rsp = __service_getDoc(req)
    else:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Function not implement'}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'None return value.'}
    # print(rsp)
    return flask.jsonify(rsp)

def __service_getDoc(req):
    code=req['code']
    content=service.getDoc(code=code)
    return {'isSuccess': True, 'content': content}
