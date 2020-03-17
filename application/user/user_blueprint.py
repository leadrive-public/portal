import flask
import flask_login
import json

from . import user_service

bp = flask.Blueprint('user', __name__, url_prefix='/user')

@bp.route('/service', methods=['POST','GET'])
def service():
    rsp = None
    try:
        req = flask.request.get_json()
        if 'function' not in req:
            raise Exception('Function is not specified.')
        func = req['function']
        if func == 'getUsers':
            rsp = __service_getUsers(req)
        elif func == 'getUser':
            rsp = __service_getUser(req)
        else:
            rsp = {'isSuccess': False, 'exceptionMessage': 'Function {} is not implemented.'.format(func)}
    except Exception as e:
        print(e)
        rsp = {'isSuccess': False, 'exceptionMessage': e}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Return value is None.'}
    return flask.jsonify(rsp)

def __service_getUsers(req):
    users=user_service.getUsers()
    if users is None:
        return None
    return {'isSuccess': True, 'users': users}

def __service_getUser(req):
    userId=int(req['id'])
    user=user_service.getUserById(userId)
    if user!=None:
        return {'isSuccess': True, 'name': user.name, 'id': userId,'displayName': user.displayName}
    else:
        return {'isSuccess': False}