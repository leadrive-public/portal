import sqlite3
import os
import flask
import json
import time
from datetime import datetime
from datetime import timedelta

from ..project import service as projectService


def databaseFilePath():
    return os.path.join(os.path.dirname(__file__), '../database/etime.sqlite3')


def getActivitiesByCode(conn=None):
    localConn = False
    if conn is None:
        try:
            localConn = True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        activities = []
        cmd = 'select code, sum(hours) from etimes where occurDate>"{}" group by code'.format(
            '2020-01-01')
        cursor = conn.execute(cmd)
        for row in cursor:
            activity = {}
            activity['code'] = row[0]
            activity['hours'] = row[1]
            activities.append(activity)
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close
    return activities


def getStatisticsByCode(conn=None):
    localConn = False
    if conn is None:
        try:
            localConn = True
            conn = sqlite3.connect(databaseFilePath())
        except:
            print('Fail to connect the database: {}!\n'.format(databaseFilePath()))
            if conn is not None:
                conn.close()
            return []
    try:
        statistics = []
        cmd = 'select code, sum(hours) from etimes group by code'
        cursor = conn.execute(cmd)
        for row in cursor:
            statistic = {}
            statistic['code'] = row[0]
            statistic['hours'] = row[1]
            statistics.append(statistic)
    except Exception as e:
        print(e)
        return []
    finally:
        if localConn:
            if conn is not None:
                conn.close
    return statistics


def getEtimes(code="", user=0, timespan=None):
    etimes = []
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
    except Exception as e:
        print(e)
        return None
    try:
        if code != "":
            if user > 0:
                cmd = 'select user, code, task, hours, occurDate from etimes where code="{}" and user={}'.format(
                    code, user)
            else:
                cmd = 'select user, code, task, hours, occurDate from etimes where code="{}"'.format(
                    code)
        else:
            if user > 0:
                cmd = 'select user, code, task, hours, occurDate from etimes where user={}'.format(
                    user)
            else:
                cmd = 'select user, code, task, hours, occurDate from etimes'
        cursor.execute(cmd)
        for row in cursor:
            occurDate = datetime.strptime(row[4], '%Y-%m-%d').date()
            if timespan is not None:
                if 'startDate' in timespan:
                    if occurDate < timespan['startDate']:
                        continue
                if 'endDate' in timespan:
                    if occurDate > timespan['endDate']:
                        continue
            etime = {}
            etime['user'] = row[0]
            etime['code'] = row[1]
            etime['task'] = row[2]
            etime['hours'] = row[3]
            etime['occurDate'] = datetime.strftime(occurDate, '%Y-%m-%d')
            etimes.append(etime)
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()
    return etimes


def getMyEditableEtimes(user):
    editableSpan = getEditableSpan()
    return None


def fillTaskTitle(etimes):
    if etimes is None:
        return
    localTasks = getLocalTasks()
    projectTasks = getProjectTasks()
    for etime in etimes:
        if etime['task'] == 0:
            etime['taskTitle'] = '非特定任务'
            continue
        etime['taskTitle'] = ''
        if etime['code'].startswith('PJ-'):
            for task in projectTasks:
                if etime['task'] == task['number'] and etime['code'] == task['code']:
                    etime['taskTitle'] = task['title']
                    break
        else:
            for task in localTasks:
                if etime['task'] == task['number'] and etime['code'] == task['code']:
                    etime['taskTitle'] = task['title']
                    break


def getFirstDayOfWeek(date):
    result = {
        0: (0, 6),  # Mon
        1: (-1, 5),  # Tue
        2: (-2, 4),  # Wed
        3: (-3, 3),  # Thu
        4: (-4, 2),  # Fri
        5: (-5, 1),  # Sat
        6: (-6, 0),  # Sun
    }
    weekDate = date+timedelta(days=result[date.weekday()][0])
    return weekDate


def getLastDayOfWeek(date):
    result = {
        0: (0, 6),  # Mon
        1: (-1, 5),  # Tue
        2: (-2, 4),  # Wed
        3: (-3, 3),  # Thu
        4: (-4, 2),  # Fri
        5: (-5, 1),  # Sat
        6: (-6, 0),  # Sun
    }
    weekDate = date+timedelta(days=result[date.weekday()][1])
    return weekDate


newWeekStartDate = -2  # SAT
newWeekStartHour = 4  # 12:00


def getEditableSpan():
    utcnow = datetime.utcnow()
    # if newWeekStartDate == -2:
    #     result = {
    #         0: (0, 6),  # MON
    #         1: (-1, 5),  # TUE
    #         2: (-2, 4),  # WED
    #         3: (-3, 3),  # THU
    #         4: (-4, 2),  # FRI
    #         5: (2, 8),  # SAT
    #         6: (1, 7),  # SUN
    #     }
    switchDate = newWeekStartDate % 7
    if utcnow.weekday() < switchDate:
        days = -utcnow.weekday()+(newWeekStartDate//7+1)*(-7)
    elif utcnow.weekday() == switchDate:
        if utcnow.hour < newWeekStartHour:
            days = -utcnow.weekday()+(newWeekStartDate//7+1)*(-7)
        else:
            days = -utcnow.weekday()+7+(newWeekStartDate//7+1)*(-7)
    else:
        days = -utcnow.weekday()+7+(newWeekStartDate//7+1)*(-7)
    startDate = utcnow.date() + timedelta(days=days)
    endDate = utcnow.date() + timedelta(days=days+6)
    return {'startDate': startDate, 'endDate': endDate}


def getLastWeekSpan():
    thisWeek = getEditableSpan()
    endDate = thisWeek['startDate']+timedelta(days=-1)
    startDate = getFirstDayOfWeek(endDate)
    return {'startDate': startDate, 'endDate': endDate}


def getCodes():
    codes = []
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        cmd = 'select code, title, status from codes'
        cursor.execute(cmd)
        for row in cursor:
            code = {}
            code['code'] = row[0]
            code['title'] = row[1]
            code['status'] = row[2]
            codes.append(code)
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    # get codes from the project
    projects = projectService.getProjects(metadatas=['status'])
    if projects is not None:
        for project in projects:
            code = {}
            code['code'] = 'PJ-'+project['code']
            code['title'] = project['title']
            code['status'] = project['status']
            if code['status'] is None:
                code['status'] = 'closed'
            if code['status'] == '':
                code['status'] = 'closed'
            if code['status'] == 'closed':
                code['status'] = 'closed'
            else:
                code['status'] = 'open'
            codes.append(code)
    # return
    return codes


def getTasks(code=''):
    tasks = []
    if code == '':
        tasks.extend(getLocalTasks())
        tasks.extend(getProjectTasks())
    elif code.startswith('PJ-'):
        tasks.extend(getProjectTasks(code))
    else:
        tasks.extend(getLocalTasks(code))
    return tasks


def getTaskDescription(code, taskNo):
    if code == None or code == '':
        return ''
    tasks = getTasks(code)
    for task in tasks:
        if task['number'] == taskNo:
            return task['title']
    return ''


def getTaskTitle(code, taskNo):
    if code == None or code == '':
        return ''
    tasks = getTasks(code)
    for task in tasks:
        if task['number'] == taskNo:
            return task['title']
    return ''


def getLocalTasks(code=''):
    tasks = []
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        if code != "":
            cmd = 'select id, code, number, title, status from tasks where code="{}"'.format(
                code)
        else:
            cmd = 'select id, code, number, title, status from tasks'
        cursor.execute(cmd)
        for row in cursor:
            task = {}
            task['id'] = row[0]
            task['code'] = row[1]
            task['number'] = row[2]
            task['title'] = row[3]
            task['status'] = row[4]
            tasks.append(task)
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return tasks


def getProjectTasks(code=''):
    tasks = []
    projects = projectService.getProjects()
    if code.startswith('PJ-'):
        projectCode = code[3:]
        projects2 = []
        for project in projects:
            if project['code'] == projectCode:
                projects2.append(project)
                break
        projects = projects2
    for project in projects:
        projectId = project['id']
        projectTasks = projectService.getTasks(
            project=projectId, metadatas=['status'])
        for projectTask in projectTasks:
            task = {}
            task['id'] = projectTask['id']
            task['code'] = 'PJ-'+project['code']
            task['number'] = projectTask['number']
            task['title'] = projectTask['title']
            task['status'] = projectTask['status']
            if task['status'] is None:
                task['status'] = 'closed'
            elif task['status'] == '':
                task['status'] = 'closed'
            elif task['status'] == 'closed':
                task['status'] = 'closed'
            else:
                task['status'] = 'open'
            if(projectTask['isGrouped'] == 1):
                continue
            tasks.append(task)
    return tasks


def delEtimes(user, timespan):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        startDateStr = datetime.strftime(timespan['startDate'], '%Y-%m-%d')
        endDateStr = datetime.strftime(timespan['endDate'], '%Y-%m-%d')
        cmd = 'delete from etimes where user={} and occurDate>="{}" and occurDate<="{}"'.format(
            user, startDateStr, endDateStr)
        cursor.execute(cmd)
        conn.commit()
    except Exception as e:
        print(str(e))
        return
    finally:
        if conn is not None:
            conn.close()
    return


def setEtimes(etimes):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        for etime in etimes:
            user = etime['user']
            code = etime['code']
            task = etime['task']
            hours = etime['hours']
            occurDate = etime['occurDate']
            cmd = 'insert into etimes (user, code, task, hours, occurDate) values({},"{}",{},{},"{}")'.format(
                user, code, task, hours, occurDate)
            cursor.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
        return
    finally:
        if conn is not None:
            conn.close()
    return


def getLastWeekHoursByUser(user):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()

        editableWeek = getEditableSpan()
        lastWeekStartDate = editableWeek['startDate']+timedelta(days=-7)
        lastWeekEndDate = editableWeek['endDate']+timedelta(days=-7)
        startDateStr = lastWeekStartDate.isoformat()[0:10]
        endDateStr = lastWeekEndDate.isoformat()[0:10]

        cmd = 'select sum(hours) from etimes where user={} and occurDate>="{}" and occurDate<="{}"'.format(
            user, startDateStr, endDateStr)
        cursor.execute(cmd)

        for row in cursor:
            return row[0]
        return 0
    except Exception as e:
        print(str(e))
        return -1
    finally:
        if conn is not None:
            conn.close()
    return


def getTotalHours(user: 'int' = -1, code: 'str' = "", task: 'int' = -1, timespan=None):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()

        cmd = 'select sum(hours) from etimes'
        condition = 0
        if user >= 0:
            if condition == 0:
                cmd = cmd+' where user={} '.format(user)
                condition += 1
            else:
                cmd = cmd+' and user={} '.format(user)
        if code != '':
            if condition == 0:
                cmd = cmd+' where code="{}" '.format(code)
                condition += 1
            else:
                cmd = cmd+' and code="{}" '.format(code)
        if task >= 0:
            if condition == 0:
                cmd = cmd+' where task={} '.format(task)
                condition += 1
            else:
                cmd = cmd+' and task={} '.format(task)
        if timespan != None:
            startDate = timespan['startDate']
            startDateStr = startDate.isoformat()[0:10]
            endDate = timespan['endDate']
            endDateStr = endDate.isoformat()[0:10]
            if condition == 0:
                cmd = cmd + \
                    ' where occurDate>="{}" and occurDate<="{}" '.format(
                        startDateStr, endDateStr)
                condition += 1
            else:
                cmd = cmd + \
                    ' and occurDate>="{}" and occurDate<="{}" '.format(
                        startDateStr, endDateStr)
        cursor.execute(cmd)
        for row in cursor:
            if row[0] != None:
                return row[0]
            else:
                return 0
        return 0
    except Exception as e:
        print(str(e))
        return -1
    finally:
        if conn is not None:
            conn.close()
    return - 1


def getStatisticsOfLastWeek():
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        lastweekSpan = getLastWeekSpan()
        startDateStr = datetime.strftime(lastweekSpan['startDate'], '%Y-%m-%d')
        endDateStr = datetime.strftime(lastweekSpan['endDate'], '%Y-%m-%d')
        statistics = []
        cmd = 'select user, sum(hours), code from etimes where occurDate>="{}" and occurDate<="{}" group by user, code order by user, code'.format(
            startDateStr, endDateStr)
        cursor.execute(cmd)
        for row in cursor:
            statistic = {}
            statistic['user'] = row[0]
            statistic['hours'] = row[1]
            statistic['code'] = row[2]
            statistics.append(statistic)
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close
    return statistics


def getStatisticsOfThisWeek():
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        lastweekSpan = getEditableSpan()
        startDateStr = datetime.strftime(lastweekSpan['startDate'], '%Y-%m-%d')
        endDateStr = datetime.strftime(lastweekSpan['endDate'], '%Y-%m-%d')
        statistics = []
        cmd = 'select user, sum(hours), code from etimes where occurDate>="{}" and occurDate<="{}" group by user, code'.format(
            startDateStr, endDateStr)
        cursor.execute(cmd)
        for row in cursor:
            statistic = {}
            statistic['user'] = row[0]
            statistic['hours'] = row[1]
            statistic['code'] = row[2]
            statistics.append(statistic)
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close
    return statistics


def getStatisticsByMonth():
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()

        lastDate = getLastWeekSpan()['endDate']
        lastDateMonth = lastDate.month
        lastDateYear = lastDate.year
        statistics = []
        for i in range(12):
            month = lastDateMonth - i
            year = lastDateYear
            if month <= 0:
                month += 12
                year = lastDateYear - 1
            startDateStr = '{:0>4d}-{:0>2d}-01'.format(year, month)
            endDateStr = '{:0>4d}-{:0>2d}-31'.format(year, month)
            cmd = 'select user, sum(hours), code from etimes where occurDate>="{}" and occurDate<="{}" group by user, code'.format(
                startDateStr, endDateStr)
            cursor.execute(cmd)
            statistics1 = []
            for row in cursor:
                statistic = {}
                statistic['user'] = row[0]
                statistic['hours'] = row[1]
                statistic['code'] = row[2]
                statistics1.append(statistic)
            statistics.append({
                'month': '{:0>4d}-{:0>2d}'.format(year, month),
                'statistics': statistics1,
            })
    except Exception as e:
        print(e)
        return []
    finally:
        if conn is not None:
            conn.close
    return statistics
