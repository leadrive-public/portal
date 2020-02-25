import flask
import flask_login
import os
import json

from . import service as service
from ..etime import service as etimeService
from ..project import service as projectService
from .. import user as userService

bp = flask.Blueprint('estaffing', __name__, url_prefix='/estaffing')

@bp.route('/')
def default():
    return flask.render_template('estaffing_home.html')

@bp.route('/service', methods=['POST','GET'])
def webService():
    req = flask.request.get_json()
    func = req['function']
    rsp = None
    if func == 'getEstaffings':
        rsp = __service_getEstaffings(req)
    else:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Function not implement'}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'None return value.'}
    # print(rsp)
    return flask.jsonify(rsp)

def __service_getEstaffings(req):
    users=user.getUsers()
    etimes=etimeService.getEtimes()
    projects=projectService.getProjectSchedules(code="")
    return None
