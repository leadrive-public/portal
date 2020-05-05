import flask
import flask_login
import json
from datetime import datetime
from datetime import timedelta

from . import service as service
from .. import user as userService

bp = flask.Blueprint('etime', __name__, url_prefix='/etime')


@bp.route('/service', methods=['POST', 'GET'])
def webService():
    rsp = None
    try:
        req = flask.request.get_json()
        if 'function' not in req:
            raise Exception('Function is not specified.')
        func = req['function']
        if func == 'getEtimes':
            rsp = __service_getEtimes(req)
        elif func == 'getMyEditableEtimes':
            rsp = __service_getMyEditableEtimes(req)
        elif func == 'setMyEditableEtimes':
            rsp = __service_setMyEditableEtimes(req)
        elif func == 'getCodes':
            rsp = __service_getCodes(req)
        elif func == 'getTasks':
            rsp = __service_getTasks(req)
        elif func == 'getStatisticsByCode':
            rsp = __service_getStatisticsByCode(req)
        elif func == 'getActivitiesByCode':
            rsp = __service_getActivitiesByCode(req)
        elif func == 'getLastWeekHoursByUser':
            rsp = __service_getLastWeekHoursByUser(req)
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
    return flask.render_template("etime/home.html", user=user)


@bp.route('/statistics')
@flask_login.login_required
def default():
    user = flask_login.current_user
    return flask.render_template("etime/statistics.html", user=user)


def __service_getEtimes(req):
    if 'code' in req:
        etimes = service.getEtimes(req['code'])
    else:
        etimes = service.getEtimes()
    if etimes is None:
        etimes = []
    return {'isSuccess': True, 'etimes': etimes}


@flask_login.login_required
def __service_getMyEditableEtimes(req):
    print("__service_getMyEditableEtimes")
    user = flask_login.current_user
    print(user)
    timespan = service.getEditableSpan()
    etimes = service.getEtimes(user=int(user.id), timespan=timespan)
    service.fillTaskTitle(etimes)
    # print(type(timespan['startDate']))
    startDate = datetime.strftime(timespan['startDate'], '%Y-%m-%d')
    endDate = datetime.strftime(timespan['endDate'], '%Y-%m-%d')
    return {'isSuccess': True, 'etimes': etimes, 'timespan': {'startDate': startDate, 'endDate': endDate}}


def __service_getCodes(req):
    print("__service_getCodes")
    rawCodes = service.getCodes()
    codes = []
    for code in rawCodes:
        if code['status'] == 'open':
            codes.append(code)
    if codes is None:
        codes = []
    return {'isSuccess': True, 'codes': codes}


def __service_getTasks(req):
    print("__service_getTasks")
    code = ''
    if 'code' in req:
        code = req['code']
    rawTasks = service.getTasks(code=code)
    tasks = []
    for task in rawTasks:
        if task['status'] == 'open':
            tasks.append(task)
    return {'isSuccess': True, 'tasks': tasks}


@flask_login.login_required
def __service_setMyEditableEtimes(req):
    print("__service_setMyEditableEtimes")
    user = flask_login.current_user
    try:
        etimes = req['etimes']
        newEtimes = []
        timespan = service.getEditableSpan()
        for etime in etimes:
            occurDate = (datetime.strptime(
                etime['occurDate'], '%Y-%m-%d')).date()
            if not(occurDate >= timespan['startDate'] and occurDate <= timespan['endDate']):
                continue
            if etime['code'] == '':
                continue
            if etime['task'] < 0:
                continue
            print(1)
            find = False
            for newEtime in newEtimes:
                if newEtime['code'] == etime['code'] and newEtime['task'] == etime['task'] and newEtime['occurDate'] == etime['occurDate']:
                    newEtime['hours'] = newEtime['hours']+etime['hours']
                    find = True
                    break
            if not find:
                newEtimes.append({
                    'code': etime['code'],
                    'task': etime['task'],
                    'user': user.id,
                    'hours': etime['hours'],
                    'occurDate': etime['occurDate']
                })

        service.delEtimes(user=int(user.id), timespan=timespan)
        service.setEtimes(newEtimes)
        rsp = {'isSuccess': True, 'etimes': newEtimes}
    except Exception as e:
        rsp = {'isSuccess': False, 'exceptionMessage': str(e)}
    return rsp


def __service_getStatisticsByCode(req):
    print("__service_getStatisticsByCode")
    statistics = service.getStatisticsByCode()
    return {'isSuccess': True, 'statistics': statistics}


def __service_getActivitiesByCode(req):
    print('__service_getActivitiesByCode')
    activities = service.getActivitiesByCode()
    return {'isSuccess': True, 'activities': activities}


def __service_getLastWeekHoursByUser(req):
    user = req['user']
    hours = service.getLastWeekHoursByUser(user)
    if hours >= 0:
        return {'isSuccess': True, 'hours': hours}
    else:
        return {'isSuccess': False}
