import sqlite3
import os
import flask
import json
import time
from datetime import datetime
from datetime import timedelta

from ..etime import service as etimeService
from .. import user as userService 

def databaseFilePath():
    return os.path.join(os.path.dirname(__file__),'../database/ioi.sqlite3')
def getFirstDayOfWeek(date):
    result={
        0: ( 0, ),
        1: (-1, ),
        2: (-2, ),
        3: (-3, ),
        4: (-4, ),
        5: (-5, ),
        6: (-6, ),
    }
    weekDate= date+timedelta(days=result[date.weekday()][0])
    return weekDate

def getTasks(user):
    editableSpan=etimeService.getEditableSpan()
    endDate=editableSpan['endDate']
    weekDate=getFirstDayOfWeek(endDate)
    weekDateStr=weekDate.isoformat()[0:10]
    etimes=etimeService.getEtimes(user=user, timespan=editableSpan)

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
    updates=getUpdates(user,timespan=editableSpan)
    for task in tasks:
        task['content']=''
        for update in updates:
            if update['code']==task['code'] and update['task']==task['task'] and update['weekDate']==weekDateStr:
                task['content']=update['content']
    return tasks, weekDateStr

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
            startDateStr=timespan['startDate'].isoformat()[0:9]
            endDateStr=timespan['endDate'].isoformat()[0:9]
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

def getUpdate(user, code, task, conn=None):
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
        editableSpan=etimeService.getEditableSpan()
        endDate=editableSpan['endDate']
        weekDate=getFirstDayOfWeek(endDate)
        weekDateStr=weekDate.isoformat()[0:10]
        cmd = 'select code, task, content, weekDate from updates where user={} and weekDate="{}" and code="{}" and task={}'.format(user, weekDateStr, code, task)
        cursor = conn.execute(cmd)
        updates=[]
        for row in cursor:
            update = {}
            update['code'] = row[0]
            update['task'] = row[1]
            update['content'] = row[2]
            update['weekDate']=row[3]
            updates.append(update)
        if len(updates)==0:
            update= {
                'code': code,
                'task': task,
                'content': '',
                'title':etimeService.getTaskDescription(code,task)
            }
        else:
            update=updates[0]
            update['title']=etimeService.getTaskDescription(code,task)
        # generate comment
        cmd = 'select content, editTime, id from updates where user={} and weekDate<"{}" and code="{}" and task={} order by weekDate DESC'.format(user, weekDateStr, code, task)
        cursor = conn.execute(cmd)
        latestUpdates=[]
        for row in cursor:
            latestUpdate = {}
            latestUpdate['user']=user
            latestUpdate['content'] = row[0]
            latestUpdate['editTime'] = row[1]
            updateId=row[2]
            cursor2=conn.cursor()
            cmd='select user, content, editTime from comments where [update]={} order by editTime ASC '.format(updateId)
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
    return update,weekDateStr,latestUpdates