import flask
import flask_login
import json
from datetime import datetime
from datetime import timedelta

from . import service as service
from .. import user as userService

bp = flask.Blueprint('dcc', __name__, url_prefix='/dcc')


@bp.route('/service', methods=['POST', 'GET'])
def webService():
    rsp = None
    try:
        req = flask.request.get_json()
        if 'function' not in req:
            raise Exception('Function is not specified.')
        func = req['function']
        if func == 'getProjects':
            rsp = __service_getProjects(req)
        elif func == 'getAllProjects':
            rsp = __service_getAllProjects(req)
        elif func == 'getCategories':
            rsp = __service_getCategories(req)
        elif func == 'create':
            rsp = __service_create(req)
        elif func == 'search':
            rsp = __service_search(req)
        elif func == 'getPart':
            rsp = __service_getPart(req)
        elif func == 'postFile':
            rsp = __service_postFile(req)
        elif func == 'savePart':
            rsp = __service_savePart(req)
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
    return flask.render_template("dcc/home.html", user=user)


@bp.route('/new')
@flask_login.login_required
def newPage():
    user = flask_login.current_user
    return flask.render_template("dcc/new.html", user=user)


@bp.route('/search')
@flask_login.login_required
def searchPage():
    user = flask_login.current_user
    return flask.render_template("dcc/search.html", user=user)


@bp.route('/parts/<string:partNumber>')
@flask_login.login_required
def partPage(partNumber):
    user = flask_login.current_user
    return flask.render_template("dcc/part.html", user=user, partNumber=partNumber)


@bp.route('/admin')
@flask_login.login_required
def adminPage():
    user = flask_login.current_user
    return flask.render_template("dcc/admin.html", user=user)


def __service_getProjects(req):
    return None


def __service_getAllProjects(req):
    projects = service.getAllProjects()
    return {'isSuccess': True, 'projects': projects}


def __service_getCategories(req):
    categories = service.getCategories()
    return {'isSuccess': True, 'categories': categories}


@flask_login.login_required
def __service_create(req):
    user = flask_login.current_user
    project = req['project']
    category = req['category']
    title = req['title']
    description = req['description']
    part = service.create(project=project, category=category,
                          title=title, description=description, user=user.id)
    return {'isSuccess': True, 'part': part}


def __service_getPart(req):
    number = req['number']
    part = service.get(number)
    return {'isSuccess': True, 'part': part}


def __service_postFile(req):
    fileData = req['fileData']
    fileType = req['fileType']
    fileId = service.postFile(fileData)
    return {'isSuccess': True, 'fileId': fileId}


def __service_savePart(req):
    number = req['number']
    title = req['title']
    attachments = req['attachments']
    service.savePart(number, title, description="", attachments=attachments)
    return {'isSuccess': True}
