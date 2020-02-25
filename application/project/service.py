import flask
import flask_login
import sqlite3
import os
import json
import datetime

def databaseFilePath():
    return os.path.join(os.path.dirname(__file__),'../database/project.sqlite3')

def getProjects(conn=None, code='', metadatas=[]):
    projects = []
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
        if code=='':
            cmd = 'select id, code, title from projects order by code'
        else:
            cmd = 'select id, code, title from projects where code="{}" order by code'.format(code)
        cursor = conn.execute(cmd)
        for row in cursor:
            project = {}
            project['id'] = row[0]
            project['code'] = row[1]
            project['title'] = row[2]
            projects.append(project)
        # get metadata
        for project in projects:
            id = project['id']
            for metadata in metadatas:
                project[metadata]=getProjectMetadata(conn=conn, id=id, path=metadata)
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close()
    return projects

def getProjectSchedules(code, conn=None):
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
        # get tasks
        code = code.upper()
        projects=getProjects(conn=conn, code=code, metadatas=['timespan', 'pm', 'se','members','status', 'budget', 'scope', 'milestones', 'deliverables', 'applicableProposalReviews', 'applicableDesignReviews','update'])
        for project in projects:
            tasks=getTasks(conn=conn, project=project['id'], metadatas=['status','owner','requirement','plan','schedule','update','budget'])
            for task in tasks:
                if task['schedule']==None:
                    task['schedule']=None
                elif task['schedule']=="":
                    task['schedule']=None
                else:
                    task['schedule']=json.loads(task['schedule'])
            project['tasks']=tasks
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close
    return projects

def getProjectMetadata(conn, id, path):
    cmd = 'select [value], user, [time] from projectMetadata where project={} and path="{}" order by time DESC'.format(id, path)
    try:
        cursor = conn.execute(cmd)
        row = cursor.fetchone()
        return row[0]
    except:
        return None

def setProjectSchedule(project,user=0):
    if project is None:
        return None
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor=conn.cursor()
        # get old project
        oldProject=getProjectSchedules(code=project['code'], conn=conn)[0]
        # update tasks
        oldTasks=oldProject['tasks']
        for order in range(len(project['tasks'])):
            project['tasks'][order]['order']=order+1
            project['tasks'][order]['project']=project['id']
        for task in project['tasks']:
            # insert new tasks
            if task['number']==-1:
                newTask=insertTask(conn=conn, task=task)
                task['id']=newTask['id']
                task['number']=newTask['number']
            else:
                newTask=updateTask(conn=conn, task=task)
        # update task metadata
        for task in project['tasks']:
            find=False
            for oldTask in oldTasks:
                if oldTask['number']==task['number']:
                    find=True
                    break
            # update status
            if find:
                if task['status']!=oldTask['status']:
                    setTaskMetadata(conn=conn, task=task['id'], path='status',value=task['status'],user=user)
            else:
                setTaskMetadata(conn=conn, task=task['id'], path='status',value=task['status'],user=user)
            #update budget
            needUpdate=False
            if find:
                if task['budget']!=oldTask['budget']:
                    needUpdate=True
            else:
                needUpdate=True
            if needUpdate:
                try:
                    value=float(task['budget'])
                except:
                    value=""
                setTaskMetadata(conn=conn, task=task['id'], path='budget',value=value,user=user)
        # update schedule
        for task in project['tasks']:
            schedule=task['schedule']
            if schedule==None:
                schedule=[]
            try:
                schedule0Str=getTaskMetadata(conn=conn,task=task['id'],path='schedule')
                schedule0=json.loads(schedule0Str)
            except:
                schedule0=[]
            # merge schedule
            schedule=getStandardSchedule(schedule)
            schedule0=getStandardSchedule(schedule0)
            equal=True
            if len(schedule)!=len(schedule0):
                equal=False
            else:
                for item in schedule:
                    find=False
                    for item2 in schedule0:
                        if item2['user']==item['user'] and item2['weekDate']==item['weekDate'] and item2['hours']==item['hours']:
                            find=True
                            break
                    if find==False:
                        equal=False
                        break
            if equal==False:
                scheduleStr=json.dumps(schedule)
                setTaskMetadata(conn=conn,task=task['id'],path='schedule',value=scheduleStr,user=user)
            pass
        
        conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return project

def getStandardSchedule(schedule):
    scheduleNew=[]
    # merge
    for item in schedule:
        find=False
        for item2 in scheduleNew:
            if item2['user']==item['user'] and item2['weekDate']==item['weekDate']:
                find=True
                break
        if find:
            item2['hours']=item2['hours']+item['hours']
        else:
            scheduleNew.append({
                'user':item['user'],
                'weekDate':item['weekDate'],
                'hours':item['hours']
            })
    return scheduleNew

def updateTask(conn, task):
    cursor=conn.cursor()
    cmd='select id,title,[order],isGrouped from tasks where project={} and number={}'.format(task['project'],task['number'])
    cursor.execute(cmd)
    result=cursor.fetchone()
    newTask={}
    newTask['id']=result[0]
    newTask['project']=task['project']
    newTask['number']=task['number']
    newTask['title']=result[1]
    newTask['order']=result[2]
    newTask['isGrouped']=result[3]
    if newTask['title']!=task['title'] or newTask['order']!=task['order'] or newTask['isGrouped']!=task['isGrouped']:
        cmd='update tasks set title="{}", [order]={}, isGrouped={} where project={} and number={}'.format(task['title'],task['order'],task['isGrouped'],task['project'],task['number'])
        cursor.execute(cmd)
        newTask['title']=task['title']
        newTask['order']=task['order']
        newTask['isGrouped']=task['isGrouped']
    return newTask

def insertTask(conn, task):
    cursor=conn.cursor()
    cmd='select max(number) from tasks where project={}'.format(task['project'])
    cursor.execute(cmd)
    result=cursor.fetchone()
    newTask={}
    newTask['project']=task['project']
    newTask['title']=task['title']
    newTask['order']=task['order']
    newTask['isGrouped']=task['isGrouped']
    if result is None:
        newTask['number']=1
    elif result[0] is None:
        newTask['number']=1
    else:
        newTask['number']=result[0]+1
    cmd='insert into tasks (project, number, title, [order], isGrouped) values({},{},"{}",{},{})'.format(newTask['project'], newTask['number'], newTask['title'], newTask['order'], newTask['isGrouped'])
    cursor.execute(cmd)
    cmd='select id from tasks where project={} and number={}'.format(newTask['project'], newTask['number'])
    cursor.execute(cmd)
    result=cursor.fetchone()
    newTask['id']=result[0]
    return newTask

def getTasks(conn=None, project=0, metadatas=[]):
    print('getTasks: project={}, metadatas={}'.format(project,metadatas))
    tasks = []
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
        if project<=0:
            cmd = 'select id, project, number, title, [order], isGrouped from tasks order by [order]'
        else:
            cmd = 'select id, project, number, title, [order], isGrouped from tasks where project={} order by [order]'.format(project)
        cursor = conn.execute(cmd)
        for row in cursor:
            task = {}
            task['id'] = row[0]
            task['project'] = row[1]
            task['number'] = row[2]
            task['title'] = row[3]
            task['order'] = row[4]
            task['isGrouped'] = row[5]
            tasks.append(task)
        for task in tasks:
            for metadata in metadatas:
                temp=getTaskMetadata(conn, task=task['id'], path=metadata)
                task[metadata]=temp
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close
    return tasks

def getTaskMetadata(conn, task, path):
    cmd = 'select value, user, time from taskMetadata where task={} and path="{}" order by time DESC'.format(task, path)
    try:
        cursor = conn.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return None
    except:
        return None
    return row[0]

def setTaskMetadata(conn, task, path, value, user, time=None):
    if time is None:
        time=datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y-%m-%d %H:%M:%S')
    cmd = 'insert into taskMetadata (task, path, value, user, time) values({},"{}",\'{}\',{},"{}")'.format(task, path, value, user, time)
    try:
        cursor = conn.execute(cmd)
    except:
        return
    return
def setProjectMetadata(conn, project, path, value, user, time=None):
    if time is None:
        time=datetime.datetime.strftime(datetime.datetime.utcnow(),'%Y-%m-%d %H:%M:%S')
    cmd = 'insert into taskMetadata (task, path, value, user, time) values({},"{}",\'{}\',{},"{}")'.format(project, path, value, user, time)
    try:
        cursor = conn.execute(cmd)
    except:
        return
    return
# projects
# id
# code
# title

# project metadata
# <project>/pm
# <project>/se
# <project>/members
# <project>/status
# <project>/budget
# <project>/scope
# <project>/milestones
# <project>/deliverables
# <project>/timespan
# <project>/applicableProposalReviews
# <project>/applicableDesignReviews
# <project>/update

# tasks
# id
# project
# number
# title
# order
# isGrouped

# task metadata
# <project>/<task>/status
# <project>/<task>/budget
# <project>/<task>/progress
# <project>/<task>/owner
# <project>/<task>/deadline
# <project>/<task>/requirement
# <project>/<task>/deliverables
# <project>/<task>/plan
# <project>/<task>/schedule=[{weekDate, user, hours}]
# <project>/<task>/update

