import flask
import flask_login
import sqlite3
import os
import json

from . import service as service

bp = flask.Blueprint('task', __name__, url_prefix='/task')


def basePath():
    return os.path.dirname(__file__)


@bp.route('/service', methods=['POST', 'GET'])
def webService():
    rsp = None
    try:
        req = flask.request.get_json()
        if 'function' not in req:
            raise Exception('Function is not specified.')
        func = req['function']
        if func == 'getAccessibleDepartments':
            rsp = __service_getAccessibleDepartments(req)
        elif func == 'getTaskTypes':
            rsp = __service_getTaskTypes(req)
        elif func == 'createTask':
            rsp = __service_createTask(req)
        else:
            rsp = {'isSuccess': False,
                   'exceptionMessage': 'Function {} is not implemented.'.format(func)}
    except Exception as e:
        print(e)
        rsp = {'isSuccess': False, 'exceptionMessage': e}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Return value is None.'}
    return flask.jsonify(rsp)


@bp.route('/')
@flask_login.login_required
def default():
    user = flask_login.current_user
    return flask.render_template('task/search.html', user=user)


@bp.route('/new')
@flask_login.login_required
def newPage():
    user = flask_login.current_user
    return flask.render_template('task/new.html', user=user)


@bp.route('/search')
@flask_login.login_required
def searchPage():
    user = flask_login.current_user
    return flask.render_template('task/search.html', user=user)


@flask_login.login_required
def __service_getAccessibleDepartments(req):
    user = flask_login.current_user
    departments = service.getAccessibleDepartments(user=user.id)
    return {'isSuccess': True, 'departments': departments}


def __service_getTaskTypes(req):
    department = req["department"]
    taskTypes = service.getTaskTypes(department=department)
    return {'isSuccess': True, 'taskTypes': taskTypes}


@flask_login.login_required
def __service_createTask(req):
    user = flask_login.current_user
    title = req['title']
    description = req['description']
    department = req['department']
    taskType = req['taskType']
    priority = req['priority']
    owner = req['owner']
    task = service.creatTask(user=user.id, title=title, description=description,
                             department=department, taskType=taskType, priority=priority, owner=owner, createBy=user.id)
    if task != None:
        return {
            'isSuccess': True,
            'taskId': task['id'],
            'title': task['title'],
            'description': task['description'],
            'department': task['department'],
            'taskType': task['taskType'],
            'priority': task['priority'],
            'owner': task['owner'],
            'status': task['status'],
            'createBy': task['createBy'],
            'createTime': task['createTime'],
        }
    else:
        return {'isSuccess': False, 'exceptionMessage': 'Fail to create the task.'}
