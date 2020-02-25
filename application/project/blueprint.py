import flask
import flask_login
import sqlite3
import os
import json

from . import service as service
from .. import user as userService

bp = flask.Blueprint('project', __name__, url_prefix='/project')

@bp.route('/')
def default():
    return flask.render_template('project_home.html')

@bp.route('/new')
@flask_login.login_required
def projectNew():
    return 'project home'

@bp.route('/schedule')
def projectSchedule():
    return flask.render_template('project_schedule.html')

@bp.route('/<string:projectCode>')
def projectDashboard(projectCode):
    return projectCode

@bp.route('/service', methods=['POST','GET'])
def webService():
    req = flask.request.get_json()
    func = req['function']
    rsp = None
    if func == 'getProjects':
        rsp = __service_getProjects(req)
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
    projects=service.getProjects(metadatas=['status','pm','se'])
    if projects is None:
        projects=[]
    return {'isSuccess': True, 'projects': projects}

def __service_getProjectSchedule(req):
    code = req['projectCode'].upper()
    projects=service.getProjectSchedules(code)
    if len(projects)<1:
        project=None
    project=projects[0]
    users=user.getUsers()
    return {'isSuccess': True, 'project': project, 'users': users}

def __service_setProjectSchedule(req):
    project=service.setProjectSchedule(req['project'],user=1)
    if project is None:
        return None
    return {'isSuccess': True, 'project': project}
    