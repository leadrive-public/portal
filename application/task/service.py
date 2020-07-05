import sqlite3
import os
import flask
import json
import time
import re
import uuid
import datetime


def databaseFilePath():
    return os.path.join(os.path.dirname(__file__), '../database/task.db3')


def getAccessibleDepartments(user):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cmd = 'select DISTINCT departments.name, departments.title from departmentAccess join departments \
            on departmentAccess.department = departments.name \
            where departmentAccess.user={}'.format(user)
        cursor = conn.cursor()
        cursor.execute(cmd)
        departments = []
        for row in cursor:
            department = {}
            department['name'] = row[0]
            department['title'] = row[1]
            departments.append(department)
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()
    return departments


def getTaskTypes(department):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cmd = 'select DISTINCT tasktype from tasktypes\
            where department="{}"'.format(department)
        cursor = conn.cursor()
        cursor.execute(cmd)
        taskTypes = []
        for row in cursor:
            taskType = row[0]
            taskTypes.append(taskType)
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()
    return taskTypes


def creatTask(user, title, description, department, taskType, priority, owner, createBy):
    try:
        conn = sqlite3.connect(databaseFilePath())
        now = datetime.datetime.utcnow()
        cmd = 'select id from tasks where id like "TK{:0>4d}____" order by id DESC LIMIT 1'.format(
            now.year)
        cursor = conn.cursor()
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            taskid = 'TK{:0>4d}0001'.format(now.year)
        else:
            index = int(row[0][6:10])
            if index == 9999:
                return None
            else:
                taskid = 'TK{:0>4d}{:0>4d}'.format(now.year, index + 1)
        createTime = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        cmd = 'insert into tasks \
            (id, title, department, tasktype, priority, owner, description, status, createby, createtime) \
            values("{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", {}, "{}") '.format(
            taskid, title, department, taskType, priority, owner, description, 'C', createBy, createTime)
        cursor.execute(cmd)
        conn.commit()
        return {
            'id': taskid,
            'title': title,
            'description': description,
            'department': department,
            'taskType': taskType,
            'status': 'C',
            'priority': priority,
            'owner': owner,
            'createBy': createBy,
            'createTime': createTime
        }
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()
    return None
