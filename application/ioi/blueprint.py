import flask
import flask_login
import json
from datetime import datetime
from datetime import timedelta

from . import service as service
from .. import user as userService

bp = flask.Blueprint('ioi', __name__, url_prefix='/ioi')

@bp.route('/service', methods=['POST','GET'])
def webService():
    rsp = None
    try:
        req = flask.request.get_json()
        if 'function' not in req:
            raise Exception('Function is not specified.')
        func = req['function']
        if func == 'getTasks':
            rsp=__service_getTasks(req)
        elif func == 'getUpdate':
            rsp=__service_getUpdate(req)
        else:
            rsp = {'isSuccess': False, 'exceptionMessage': 'Function {} is not implemented.'.format(func)}
    except Exception as e:
        print(e)
        rsp = {'isSuccess': False, 'exceptionMessage': e}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Return value is None.'}
    return flask.jsonify(rsp)

@bp.route('/')
@flask_login.login_required
def default():
    user=flask_login.current_user
    return flask.render_template('ioi_home.html', user=user)

@bp.route('/updates')
@flask_login.login_required
def updatesPage():
    user=flask_login.current_user
    return flask.render_template("ioi_updates.html", user=user)

@bp.route('/edit')
@flask_login.login_required
def editPage():
    user=flask_login.current_user
    code=flask.request.args.get('code')
    task=0
    return flask.render_template("ioi_edit.html", user=user, code=code, task=task)

@bp.route('/teams')
@flask_login.login_required
def teamsPage():
    user=flask_login.current_user
    return flask.render_template("ioi_teams.html", user=user)

@bp.route('/teams/<string:team>')
@flask_login.login_required
def teamPage(team):
    user=flask_login.current_user
    return flask.render_template("ioi_team.html", user=user, team=team)

@bp.route('/projects')
@flask_login.login_required
def projectsPage():
    user=flask_login.current_user
    return flask.render_template("ioi_projects.html", user=user)

@bp.route('/projects/<string:project>')
@flask_login.login_required
def projectPage(project):
    user=flask_login.current_user
    return flask.render_template("ioi_project.html", user=user, project=project)

@bp.route('/users/<int:targetUserId>')
@flask_login.login_required
def usersPage(targetUserId):
    user=flask_login.current_user
    return flask.render_template("ioi_user.html", user=user, targetUserId=targetUserId)

@bp.route('/users/<int:targetUserId>/<string:project>/<int:task>')
@flask_login.login_required
def viewPage(targetUserId, project, task):
    user=flask_login.current_user
    return flask.render_template("ioi_view.html", user=user, targetUserId=targetUserId, project=project, task=task)

@bp.route('/users/<int:targetUserId>/<string:project>/<int:task>/<string:weekDate>')
@flask_login.login_required
def view2Page(targetUserId, project, task, weekDate):
    user=flask_login.current_user
    return flask.render_template("ioi_view.html", user=user, targetUserId=targetUserId, project=project, task=task, weekDate=weekDate)

@bp.route('/users/<int:targetUserId>/<string:project>/<int:task>/history')
@flask_login.login_required
def historyPage(targetUserId):
    user=flask_login.current_user
    return flask.render_template("ioi_view.html", user=user, targetUserId=targetUserId)

@flask_login.login_required
def __service_getTasks(req):
    user=flask_login.current_user
    tasks, weekDateStr=service.getTasks(int(user.id))
    return {'isSuccess': True, 'tasks': tasks, 'weekDate': weekDateStr}

@flask_login.login_required
def __service_getUpdate(req):
    user=flask_login.current_user
    code=req['code']
    task=int(req['task'])
    update, weekDateStr, latestUpdates=service.getUpdate(int(user.id),code=code, task=task)
    return {'isSuccess': True, 'update': update, 'weekDate': weekDateStr, 'latestUpdates': latestUpdates}