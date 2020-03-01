import flask
import flask_login
import sqlite3
import os
import json

from . import service as service
from .. import user as userService

bp = flask.Blueprint('project', __name__, url_prefix='/project')

def basePath():
    return os.path.dirname(__file__)

@bp.route('/')
@flask_login.login_required
def default():
    user=flask_login.current_user
    return flask.render_template('project_list.html', user=user, list='all')

@bp.route('/participated')
@flask_login.login_required
def participated():
    user=flask_login.current_user
    return flask.render_template('project_list.html', user=user, list='participated')

@bp.route('/managed')
@flask_login.login_required
def managed():
    user=flask_login.current_user
    return flask.render_template('project_list.html', user=user, list='managed')

@bp.route('/all')
@flask_login.login_required
def all():
    user=flask_login.current_user
    return flask.render_template('project_list.html', user=user, list='all')

# @bp.route('/new')
# @flask_login.login_required
# def projectNew():
#     return 'project home'

# @bp.route('/schedule')
# @flask_login.login_required
# def projectSchedule():
#     user=flask_login.current_user
#     return flask.render_template('project_list.html', user=user)

@bp.route('/<string:projectCode>')
@flask_login.login_required
def projectDashboard(projectCode):
    user=flask_login.current_user
    return flask.render_template('project_schedule.html', user=user, projectCode=projectCode)

@bp.route('/service', methods=['POST','GET'])
def webService():
    req = flask.request.get_json()
    func = req['function']
    rsp = None
    if func == 'getProjects':
        rsp = __service_getProjects(req)
    if func == 'getProjectList':
        rsp = __service_getProjectList(req)
    elif func == 'getProjectSchedule':
        rsp = __service_getProjectSchedule(req)
    elif func == 'setProjectSchedule':
        rsp = __service_setProjectSchedule(req)
    else:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Function not implement'}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'None return value.'}
    # print(rsp)
    return flask.jsonify(rsp)

def __service_getProjects(req):
    projects=service.getProjects(metadatas=['status','pm','se','stage','budget'])
    if projects is None:
        projects=[]
    return {'isSuccess': True, 'projects': projects}

def __service_getProjectSchedule(req):
    code = req['projectCode'].upper()
    project=service.getProjectSchedule(code)
    if project==None:
        return None
    return {'isSuccess': True, 'project': project}

def __service_setProjectSchedule(req):
    project=service.setProjectSchedule(req['project'],user=1)
    if project is None:
        return None
    return {'isSuccess': True, 'project': project}

def __service_getProjectList(req):
    projects=service.getProjectList()
    if projects is None:
        projects=[]
    return {'isSuccess': True, 'projects': projects}