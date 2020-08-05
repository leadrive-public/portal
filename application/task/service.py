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
            (id, title, department, tasktype, priority, owner, description, status, createby, createtime, updatetime) \
            values("{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", {}, "{}", "{}") '.format(
            taskid, title, department, taskType, priority, owner, description, 'C', createBy, createTime, createTime)
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
            'createTime': createTime,
            'updateTime': createTime
        }
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()
    return None


def searchTasks(user: int, taskIdStartIndex: int, taskIdEndIndex: int, department: str, taskType: str, priority: str, owner: int, status: str):
    accessibleDepartments = getAccessibleDepartments(user)
    if not(department.upper() in accessibleDepartments):
        return []
    try:
        conn = sqlite3.connect(databaseFilePath())
        cmd = 'select (id, title, department, tasktype, priority, owner, description, status, createby, createtime, updateTime from tasks where \
                id >= "TK{:0>8d}" and id <= "TK{:0>8d}" and department = "{}" '.format(taskIdStartIndex, taskIdEndIndex, department)
        if taskType != "":
            cmd = cmd + ' and taskType="{}"'.format(taskType)
        if priority != "":
            cmd = cmd + ' and priority="{}"'.format(priority)
        if owner != 0:
            cmd = cmd + ' and owner={}'.format(owner)
        if status != "":
            cmd = cmd + ' and status="{}"'.format(status)
        cursor = conn.cursor()
        cursor.execute(cmd)
        tasks = []
        for row in cursor:
            task = {
                'taskId': row[0],
                'title': row[1],
                'department': row[2],
                'taskType': row[3],
                'priority': row[4],
                'owner': row[5],
                'description': row[6],
                'status': row[7],
                'createBy': row[8],
                'createTime': row[9],
                'updateTime': row[10]
            }
            tasks.append(task)
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close()
    return tasks
