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
        if func == 'getTasksOfThisWeek':
            rsp=__service_getTasksOfThisWeek(req)
        elif func == 'getUpdate':
            rsp=__service_getUpdate(req)
        elif func == 'getUpdateOfThisWeek':
            rsp=__service_getUpdateOfThisWeek(req)
        elif func == 'getUpdateOfLastWeek':
            rsp=__service_getUpdateOfLastWeek(req)
        elif func == 'getAuthorizedTeams':
            rsp=__service_getAuthorizedTeams(req)
        elif func == 'getAuthorizedProjects':
            rsp=__service_getAuthorizedProjects(req)
        elif func == 'getTeamMembers':
            rsp=__service_getTeamMembers(req)
        elif func == 'getTasksOfLastWeek':
            rsp=__service_getTasksOfLastWeek(req)
        elif func == 'postUpdateOfThisWeek':
            rsp=__service_setUpdateOfThisWeek(req)
        elif func == 'getProjectStatisticsOfLastWeek':
            rsp=__service_getProjectStatisticsOfLastWeek(req)
        elif func == 'postComment':
            rsp=__service_postComment(req)
        else:
            rsp = {'isSuccess': False, 'exceptionMessage': 'Function {} is not implemented.'.format(func)}
    except Exception as e:
        print(e)
        rsp = {'isSuccess': False, 'exceptionMessage': e}
    if rsp is None:
        rsp = {'isSuccess': False, 'exceptionMessage': 'Return value is None.'}
    return flask.jsonify(rsp)

# /
# /my/edit
# /my/lastweek
# /teams
# /teams/EV-ENG-HW/lastweek
# /projects
# /projects/EV0004/lastweek
# /users/1/lastweek
# /users/1/view?code=EV0004&task=1&weekDate=2020-01-01
# /users/1/history?code=EV0004&task=1
@bp.route('/')
@flask_login.login_required
def default():
    user=flask_login.current_user
    return flask.render_template('ioi_home.html', user=user)

@bp.route('/my/edit')
@flask_login.login_required
def myEditPage():
    user=flask_login.current_user
    code=flask.request.args.get('code')
    task=flask.request.args.get('task')
    if(code==None or task==None):
        return flask.render_template('ioi_edit_home.html',user=user)
    return flask.render_template('ioi_edit.html', user=user, code=code, task=task)

@bp.route('/my/lastweek')
@flask_login.login_required
def myListPage():
    user=flask_login.current_user
    return flask.render_template("ioi_lastweek.html", user=user)

@bp.route('/teams')
@flask_login.login_required
def teamsPage():
    user=flask_login.current_user
    return flask.render_template("ioi_teams.html", user=user)

@bp.route('/teams/<string:team>/lastweek')
@flask_login.login_required
def teamListPage(team):
    user=flask_login.current_user
    return flask.render_template("ioi_team_lastweek.html", user=user, team=team)

@bp.route('/projects')
@flask_login.login_required
def projectsPage():
    user=flask_login.current_user
    return flask.render_template("ioi_projects.html", user=user)

@bp.route('/projects/<string:project>/lastweek')
@flask_login.login_required
def projectListPage(project):
    user=flask_login.current_user
    return flask.render_template("ioi_project_lastweek.html", user=user, project=project)

@bp.route('/users/<int:targetUserId>/lastweek')
@flask_login.login_required
def userListPage(targetUserId):
    user=flask_login.current_user
    return flask.render_template("ioi_user_lastweek.html", user=user, targetUserId=targetUserId)

@bp.route('/users/<int:targetUserId>/view')
@flask_login.login_required
def viewPage(targetUserId):
    user=flask_login.current_user
    code=flask.request.args.get('code')
    task=flask.request.args.get('task')
    weekDateStr=flask.request.args.get('weekDate')
    if(code==None or task==None or weekDateStr==None):
        return 'errorPage'
    weekDate=datetime.fromisoformat(weekDateStr)
    return flask.render_template("ioi_view.html", user=user, targetUserId=targetUserId, project=code, task=task, weekDate=weekDate)

@bp.route('/users/<int:targetUserId>/history')
@flask_login.login_required
def view2Page(targetUserId):
    user=flask_login.current_user
    code=flask.request.args.get('code')
    task=flask.request.args.get('task')
    if(code==None or task==None):
        return 'errorPage'
    return flask.render_template("ioi_history.html", user=user, targetUserId=targetUserId, project=code, task=task)

@flask_login.login_required
def __service_getTasksOfThisWeek(req):
    user=flask_login.current_user
    tasks, weekDate=service.getTasksOfThisWeek(int(user.id))
    return {'isSuccess': True, 'tasks': tasks, 'weekDate': weekDate.isoformat()[0:10]}

@flask_login.login_required
def __service_getAuthorizedTeams(req):
    user=flask_login.current_user
    teams=service.getAuthorizedTeams(int(user.id))
    return {'isSuccess': True, 'teams': teams}

def __service_getTeamMembers(req):
    team=req['team']
    members=service.getTeamMembers(team)
    return {'isSuccess': True, 'members': members}

def __service_getTasksOfLastWeek(req):
    user=int(req['user'])
    tasks, weekDate=service.getTasksOfLastWeek(user)
    return {'isSuccess': True, 'tasks': tasks, 'weekDate': weekDate.isoformat()[0:10]}

def __service_getUpdateOfLastWeek(req):
    user=int(req['user'])
    code=req['code']
    task=int(req['task'])
    update, weekDate, latestUpdates=service.getUpdateOfLastWeek(user=user,code=code, task=task)
    return {'isSuccess': True, 'update': update, 'weekDate': weekDate.isoformat()[0:10], 'latestUpdates': latestUpdates}

@flask_login.login_required
def __service_getUpdateOfThisWeek(req):
    user=int(flask_login.current_user.id)
    code=req['code']
    task=int(req['task'])
    update, weekDate, latestUpdates=service.getUpdateOfThisWeek(user,code=code, task=task)
    return {'isSuccess': True, 'update': update, 'weekDate': weekDate.isoformat()[0:10], 'latestUpdates': latestUpdates}

@flask_login.login_required
def __service_getUpdate(req):
    user=int(req['user'])
    code=req['code']
    task=int(req['task'])
    weekDateStr=req['weekDate']
    weekDate=datetime.fromisoformat(weekDateStr)
    update, weekDate, latestUpdates=service.getUpdate(user=user,code=code, task=task, weekDate=weekDate)
    return {'isSuccess': True, 'update': update, 'weekDate': weekDate.isoformat()[0:10], 'latestUpdates': latestUpdates}

@flask_login.login_required
def __service_setUpdateOfThisWeek(req):
    user=int(flask_login.current_user.id)
    code=req['code']
    task=req['task']
    content=req['content']
    weekDateStr=req['weekDate']
    weekDate=datetime.fromisoformat(weekDateStr)
    service.setUpdateOfThisWeek(user=user, code=code, task=task, weekDate=weekDate, content=content)
    return {'isSuccess':True}

@flask_login.login_required
def __service_postComment(req):
    user=int(flask_login.current_user.id)
    update=req['update']
    content=req['content']
    service.postComment(update=update, user=user, content=content)
    return {'isSuccess':True}

@flask_login.login_required
def __service_getAuthorizedProjects(req):
    user=int(flask_login.current_user.id)
    projects=service.getAuthorizedProjects(user)
    return {'isSuccess': True, 'projects': projects}

def __service_getProjectStatisticsOfLastWeek(req):
    project=req['project']
    items=service.getProjectStatisticsOfLastWeek(project=project)
    return {'isSuccess': True, 'items': items}