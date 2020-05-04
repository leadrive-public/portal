import sqlite3
import os
import flask
import json
import time
import re
import uuid
from datetime import datetime

from ..project import service as projectService


def databaseFilePath():
    return os.path.join(os.path.dirname(__file__), '../database/dcc.sqlite3')


def fileStoragePath():
    return os.path.join(os.path.dirname(__file__), '../database/dcc/')


def getAllProjects():
    allProjects = projectService.getProjects(conn=None, code='', metadatas=[])
    projects = []
    for project in allProjects:
        if re.match('^[a-zA-Z]{2}[0-9]{4}$', project['code']) == None:
            continue
        projects.append({
            'code': project['code'],
            'title': project['title'],
        })
    return projects


def getCategories():
    try:
        conn = sqlite3.connect(databaseFilePath())
        cmd = 'select code, title from categories order by code'
        cursor = conn.cursor()
        cursor.execute(cmd)
        categories = []
        for row in cursor:
            category = {}
            category['code'] = row[0]
            category['title'] = row[1]
            categories.append(category)
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return categories


def create(project: str, category: str, title: str, description: str, user: int):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        cmd = 'select number from parts where number like "{}-{}%" order by number DESC'.format(
            project.upper(), category.upper())
        cursor.execute(cmd)
        result = cursor.fetchone()
        if result == None:
            index = 1
        else:
            index = int(result[0][9:13])
            index = index + 1
            if index > 9999:
                return ""
        number = '{}-{}{:0>4d}-01'.format(project.upper(),
                                          category.upper(), index)
        cmd = 'insert into parts (number, title, description, status, createBy, createTime) values("{}","{}","{}","{}",{},"{}")'.format(
            number, title, description, 'C', user, datetime.utcnow().isoformat()[0:19])
        cursor.execute(cmd)
        conn.commit()
        cmd = 'select id, number, title, description, status, createBy, createTime, releaseBy, releaseTime from parts where number="{}"'.format(
            number)
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return None
        part = {
            'id': row[0],
            'number': row[1],
            'title': row[2],
            'description': row[3],
            'status': row[4],
            'createBy': row[5],
            'createTime': row[6],
            'releaseBy': row[7],
            'releaseTime': row[8],
        }
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return part


def get(number: str):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        cmd = 'select id, number, title, description, status, createBy, createTime, releaseBy, releaseTime from parts where number="{}"'.format(
            number)
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return None
        part = {
            'id': row[0],
            'number': row[1],
            'title': row[2],
            'description': row[3],
            'status': row[4],
            'createBy': row[5],
            'createTime': row[6],
            'releaseBy': row[7],
            'releaseTime': row[8],
        }
        cmd = 'select id, name, size from attachments where part={}'.format(
            part['id'])
        cursor.execute(cmd)
        attachments = []
        for row in cursor:
            attachment = {
                'id': row[0],
                'name': row[1],
                'size': row[2],
            }
            attachments.append(attachment)
        part['attachments'] = attachments
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return part


def postFile(fileData):
    # generate uuid
    id = uuid.uuid1()
    # save
    return id


def savePart(number: str, title: str, description: str, attachments):
    try:
        conn = sqlite3.connect(databaseFilePath())
        cursor = conn.cursor()
        # update title
        cmd = 'select title from parts where number="{}"'.format(number)
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return False
        if title != row[0]:
            cmd = 'update parts set title="{}" where number="{}"'.format(
                title, number)
            cursor.execute(cmd)
        # update description
        cmd = 'select description from parts where number="{}"'.format(number)
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return False
        if title != row[0]:
            cmd = 'update parts set description="{}" where number="{}"'.format(
                description, number)
            cursor.execute(cmd)
        conn.commit()
        # update attachments
        cmd = 'select id from parts where number="{}"'.format(number)
        cursor.execute(cmd)
        row = cursor.fetchone()
        if row == None:
            return False
        partId = row[0]
        cmd = 'select id from attachments where part={}'.format(
            partId)
        cursor.execute(cmd)
        toDeleteAttachments = []
        for row in cursor:
            attachmentId = row[0]
            find = False
            for attachment in attachments:
                if attachment['id'] == attachmentId:
                    find = True
                    break
            if find == False:
                toDeleteAttachments.append(attachmentId)
        for attachmentId in toDeleteAttachments:
            cmd = 'delete from attachments where id="{}"'.format(
                attachmentId)
            cursor.execute(cmd)
            delFile(attachmentId)
        for attachment in attachments:
            if attachment['id'] == "":
                attachmentId = str(uuid.uuid1())
                createFile(attachmentId, attachment['content'])
                cmd = 'insert into attachments (id, name, size, part) values("{}", "{}", {}, {})'.format(
                    attachmentId, attachment['name'], attachment['size'], partId)
                cursor.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
        return None
    finally:
        if conn is not None:
            conn.close()
    return True


def delFile(id: str):
    filePath = os.path.join(fileStoragePath(), id)
    if os.path.exists(filePath):
        os.remove(filePath)


def createFile(id: str, content):
    filePath = os.path.join(fileStoragePath(), id)
    if os.path.exists(filePath):
        os.remove(filePath)
    file = open(filePath, 'wb')
    file.write(bytes(content))
    file.close()
