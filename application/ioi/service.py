import sqlite3
import os
import flask
import json
import time
from datetime import datetime
from datetime import timedelta

from ..etime import service as etimeService
from .. import user as userService
from .. import mail

def databaseFilePath():
    return os.path.join(os.path.dirname(__file__),'../database/ioi.sqlite3')
def getFirstDayOfWeek(date):
    result={
        0: ( 0, 6), # Mon
        1: (-1, 5), # Tue
        2: (-2, 4), # Wed
        3: (-3, 3), # Thu
        4: (-4, 2), # Fri
        5: (-5, 1), # Sat
        6: (-6, 0), # Sun
    }
    weekDate= date+timedelta(days=result[date.weekday()][0])
    return weekDate
def getLastDayOfWeek(date):
    result={
        0: ( 0, 6), # Mon
        1: (-1, 5), # Tue
        2: (-2, 4), # Wed
        3: (-3, 3), # Thu
        4: (-4, 2), # Fri
        5: (-5, 1), # Sat
        6: (-6, 0), # Sun
    }
    weekDate= date+timedelta(days=result[date.weekday()][1])
    return weekDate
def getTasksOfThisWeek(user):
    weekDate=etimeService.getEditableSpan()['startDate']
    tasks=getTasks(user=user, weekDate=weekDate)
    return tasks, weekDate
def getTasksOfLastWeek(user):
    weekDate=etimeService.getEditableSpan()['startDate']
    weekDate=weekDate+timedelta(days=-7)
    tasks=getTasks(user=user, weekDate=weekDate)
    return tasks, weekDate
def getTasks(user,weekDate):
    timespan={
        'startDate': getFirstDayOfWeek(weekDate),
        'endDate': getLastDayOfWeek(weekDate)
    }
    weekDateStr=weekDate.isoformat()[0:10]
    etimes=etimeService.getEtimes(user=user, timespan=timespan)

    tasks=[]
    for etime in etimes:
        find=False
        for task in tasks:
            if task['code']==etime['code'] and task['task']==etime['task']:
                task['hours']+=etime['hours']
                find=True
                break
        if not find:
            tasks.append({
                'code':etime['code'],
                'task':etime['task'],
                'hours':etime['hours'],
                'title':etimeService.getTaskDescription(etime['code'],etime['task'])
            })
    updates=getUpdates(user,timespan=timespan)
    for task in tasks:
        task['content']=''
        for update in updates:
            if update['code']==task['code'] and update['task']==task['task'] and update['weekDate']==weekDateStr:
                task['content']=update['content']
    return tasks

def getUpdates(user,timespan=None,conn=None):
    localConn=False
    if conn is None:
        try:
            localConn=True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        if timespan==None:
            cmd = 'select code, task, content, weekDate from updates where user={}'.format(user)
        else:
            startDateStr=timespan['startDate'].isoformat()[0:10]
            endDateStr=timespan['endDate'].isoformat()[0:10]
            cmd = 'select code, task, content, weekDate from updates where user={} and weekDate>="{}" and weekDate<="{}"'.format(user, startDateStr, endDateStr)
        cursor = conn.execute(cmd)
        updates=[]
        for row in cursor:
            update = {}
            update['code'] = row[0]
            update['task'] = row[1]
            update['content'] = row[2]
            update['weekDate']=row[3]
            updates.append(update)
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close()
    return updates
def getUpdateOfLastWeek(user, code, task):
    weekDate=etimeService.getEditableSpan()['startDate']
    weekDate=weekDate+timedelta(days=-7)
    update, latestUpdate=getUpdate(user=user, code=code, task=task, weekDate=weekDate)
    return update, weekDate, latestUpdate
def getUpdateOfThisWeek(user, code, task):
    weekDate=etimeService.getEditableSpan()['startDate']
    update, latestUpdate=getUpdate(user=user, code=code, task=task, weekDate=weekDate)
    return update, weekDate, latestUpdate
def getUpdate(user, code, task, weekDate, conn=None):
    localConn=False
    if conn is None:
        try:
            localConn=True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        weekDateStr=weekDate.isoformat()[0:10]
        timespan={
            'startDate':getFirstDayOfWeek(weekDate),
            'endDate':getLastDayOfWeek(weekDate),
        }
        cmd = 'select code, task, content, weekDate, editTime, user, id from updates where user={} and weekDate="{}" and code="{}" and task={}'.format(user, weekDateStr, code, task)
        cursor = conn.execute(cmd)
        updates=[]
        for row in cursor:
            update = {}
            update['code'] = row[0]
            update['task'] = row[1]
            update['content'] = row[2]
            update['weekDate']=row[3]
            update['editTime']=row[4]
            update['user']=row[5]
            update['id']=row[6]
            updates.append(update)
        if len(updates)==0:
            update= {
                'code': code,
                'task': task,
                'content': '',
                'title':etimeService.getTaskDescription(code,task),
                'hours':etimeService.getTotalHours(user=user, code=code, task=task, timespan=timespan),
                'weekDate':weekDateStr,
                'editTime':"",
                'user':user,
                'comments':[],
                'id':-1,
            }
        else:
            update=updates[0]
            update['title']=etimeService.getTaskDescription(code,task)
            update['hours']=etimeService.getTotalHours(user=user, code=code, task=task, timespan=timespan)
            # generate comment
            cmd='select user, content, editTime from comments where [update]={} order by editTime ASC '.format(update['id'])
            cursor.execute(cmd)
            comments=[]
            for row in cursor:
                comment = {}
                comment['user']=row[0]
                comment['content'] = row[1]
                comment['editTime'] = row[2]
                comments.append(comment)
            update['comments']=comments

        # generate latestUpdates
        cmd = 'select code, task, content, weekDate, editTime, user, id from updates where user={} and weekDate<"{}" and code="{}" and task={} order by weekDate DESC'.format(user, weekDateStr, code, task)
        cursor.execute(cmd)
        latestUpdates=[]
        for row in cursor:
            latestUpdate = {}
            latestUpdate['code'] = row[0]
            latestUpdate['task'] = row[1]
            latestUpdate['content'] = row[2]
            latestUpdate['weekDate']=row[3]
            latestUpdate['editTime']=row[4]
            latestUpdate['user']=row[5]
            latestUpdate['id']=row[6]
            latestUpdate['title']=etimeService.getTaskDescription(code,task)
            timespan={
                'startDate':getFirstDayOfWeek(datetime.fromisoformat(latestUpdate['weekDate'])),
                'endDate':getLastDayOfWeek(datetime.fromisoformat(latestUpdate['weekDate'])),
            }
            latestUpdate['hours']=etimeService.getTotalHours(user=user, code=code, task=task, timespan=timespan)
            cursor2=conn.cursor()
            cmd='select user, content, editTime from comments where [update]={} order by editTime ASC '.format(latestUpdate['id'])
            cursor2.execute(cmd)
            comments=[]
            for row2 in cursor2:
                comment = {}
                comment['user']=row2[0]
                comment['content'] = row2[1]
                comment['editTime'] = row2[2]
                comments.append(comment)
            latestUpdate['comments']=comments
            latestUpdates.append(latestUpdate)
            break
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close()
    return update,latestUpdates

def getAuthorizedTeams(user:'int', conn=None):
    localConn=False
    if conn is None:
        try:
            localConn=True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        cmd='''
            select tb1.team, tb1.members from 
            (select team, count(user) as members from teamChart where role="M" group BY team) as tb1 inner join 
            (select team, user from teamChart where role="A" and user={}) as tb2 on tb1.team=tb2.team 
            '''.format(user)
        cursor = conn.execute(cmd)
        teams=[]
        for row in cursor:
            team = {}
            team['name'] = row[0]
            team['members'] = row[1]
            teams.append(team)
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close()
    return teams

def getTeamMembers(team:'str', conn=None):
    localConn=False
    if conn is None:
        try:
            localConn=True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        cmd='''SELECT user from teamChart where team="{}" and role="M"'''.format(team)
        cursor = conn.execute(cmd)
        members=[]
        for row in cursor:
            members.append(row[0])
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close()
    return members

def setUpdateOfThisWeek(user:'int', code:'str', task:'int', weekDate:'datetime', content:'str'):
    try:
        conn=sqlite3.connect(databaseFilePath())
        cursor=conn.cursor()
        cmd='select id from updates where user={} and code="{}" and task={} and weekDate="{}"'.format(user,code,task,weekDate.isoformat()[0:10])
        cursor.execute(cmd)
        id=-1
        for row in cursor:
            id=row[0]
        if id>=0:
            cmd='update updates set content="{}" where id={}'.format(content, id)
        else:
            cmd='insert into updates (user, code, task, weekDate, content, editTime) values({},"{}",{},"{}","{}","{}")'.format(user,code,task,weekDate.isoformat()[0:10],content,datetime.utcnow().isoformat()[0:19])
        cursor.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
        return False
    finally:
        if conn!=None:
            conn.close()
    return True

def postComment(user:'int',update:'int',content:'str'):
    if user<=0:
        return False
    try:
        conn=sqlite3.connect(databaseFilePath())
        cursor=conn.cursor()
        editTime=datetime.utcnow().isoformat()[0:19]
        cmd='insert into comments (user, [update], content, editTime) values({},{},"{}","{}")'.format(user,update,content,editTime)
        cursor.execute(cmd)
        conn.commit()

        posts=[]

        cmd='select user, content, editTime from comments where [update]={} order by editTime DESC'.format(update)
        cursor.execute(cmd)
        for row in cursor:
            posts.append({
                'author': row[0],
                'content': row[1],
                'editTime': row[2],
            })
        cmd='select user,content, editTime, code, task, weekDate from updates where id={}'.format(update)
        cursor.execute(cmd)
        for row in cursor:
            posts.append({
                'author': row[0],
                'content': row[1],
                'editTime': row[2],
            })
            code=row[3]
            task=row[4]
            weekDate=row[5]
            postOwner=row[0]

        body='''
        <style>
        p{{margin:0;}}
        pre{{margin:0;}}
        </style>
        <p><strong>WeekDate: {}</strong></p>
        <p><strong>Project: {}</strong></p>
        <p><strong>Task: {}</strong></p>
        '''.format(weekDate, code, task)
        body+='''
        <a href="http://portal.leadrive.com/ioi/users/{}/view?code={}&task={}&weekDate={}">Click the link to view the details online.</a>
        <hr />
        '''.format(postOwner,code,task,weekDate)
        receivers=[]
        postIndex=0
        for post in posts:
            postIndex+=1
            author=userService.getUserById(post['author'])
            if receivers.count(author.name)==0:
                receivers.append(author.name)
            body+='''
            <p><strong>{}</strong>&nbsp;<small>{}</small></p>
            <pre>{}</pre>
            <br />'''.format(author.displayName, post['editTime'], post['content'])
            if postIndex==1:
                subject='{}在IOI中添加了评论'.format(author.displayName)

        mail.sendEmail(receivers=receivers,subject=subject,content=body, sender='etime@leadrive.com')
    except Exception as e:
        print(e)
        return False
    finally:
        if conn!=None:
            conn.close()
    return True

def getAuthorizedProjects(user:'int'):
    projects=etimeService.getCodes()
    for project in projects:
        timespan=etimeService.getLastWeekSpan()
        project['hours']=etimeService.getTotalHours(code=project['code'], timespan=timespan)
    return projects

def getProjectStatisticsOfLastWeek(project:'str'):
    timespan=etimeService.getLastWeekSpan()
    etimes=etimeService.getEtimes(code=project,timespan=timespan)
    items=[]
    for etime in etimes:
        find=False
        for item in items:
            if item['task']==etime['task'] and item['user']==etime['user']:
                item['hours']+=etime['hours']
                find=True
                break
        if not find:
            items.append({
                'task':etime['task'],
                'user':etime['user'],
                'hours':etime['hours'],
                'project':project,
                'weekDate':timespan['startDate'].isoformat()
            })
    for item in items:
        user=userService.getUserById(item['user'])
        if user==None:
            item['userName']=item['user']
        else:
            item['userName']=user.displayName
        item['taskTitle']=etimeService.getTaskTitle(code=project,taskNo=item['task'])
    return items
        