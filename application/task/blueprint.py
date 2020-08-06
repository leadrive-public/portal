from flask import render_template, request, session
from flask import Blueprint
import flask
import flask_login
import time
import datetime
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# sys.path.append('../')

# Basic function
from ..app import db
from ..mail import sendEmail
# register blueprint
bp = flask.Blueprint('task', __name__)


# table record all the task and its property
class c_task_list(db.Model):
    __tablename__ = 'tb_task_list'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    task_id = db.Column(db.String(10))
    task_name = db.Column(db.String(200))
    pj_dpt = db.Column(db.String(20))
    task_type = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    owner = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    task_status = db.Column(db.String(20))
    log_by = db.Column(db.String(20))
    log_time = db.Column(db.String(20))
    update_time = db.Column(db.String(20))


# table record the update of the task
class c_task_content(db.Model):
    __tablename__ = 'tb_task_content'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    task_id = db.Column(db.String(10))
    task_seq = db.Column(db.Integer)
    update_name = db.Column(db.String(20))
    update_time = db.Column(db.String(20))
    time_consume = db.Column(db.Float)
    content = db.Column(db.String(2000))
    task_status = db.Column(db.String(20))
    file_qty = db.Column(db.Integer)


# table record the task property change for history tracking
class c_task_log(db.Model):
    __tablename__ = 'tb_task_log'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    task_id = db.Column(db.String(10))
    property = db.Column(db.String(20))
    name = db.Column(db.String(20))
    change_time = db.Column(db.String(20))
    old = db.Column(db.String(500))
    new = db.Column(db.String(500))


# table record the setting of the system
class c_task_config(db.Model):
    __tablename__ = 'tb_task_config'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    property = db.Column(db.String(20))
    setting = db.Column(db.String(20))


# table record the user access right
class c_task_role(db.Model):
    __tablename__ = 'tb_task_role'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    user_name = db.Column(db.String(20))
    property = db.Column(db.String(20))
    value = db.Column(db.String(20))


# table record the user's email
class c_task_user(db.Model):
    __tablename__ = 'tb_task_user'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    user_name = db.Column(db.String(20))
    email = db.Column(db.String(30))


def is_access(user_name, property1, val):
    result = 0
    if user_name:
        if val:
            filters = {
                c_task_role.user_name == user_name,
                c_task_role.property == property1,
                c_task_role.value == val
            }
            all_results = c_task_role.query.filter(*filters).all()
            if all_results:  # the resource's property user access match to the settinig
                result = 1
    return result


def send_email(title, task_id, content):
    try:
        all_results = c_task_list.query.filter(
            c_task_list.task_id == task_id).first()
        if all_results:
            to_addr = []
            user = c_task_user.query.filter(
                c_task_user.user_name == all_results.owner).first()
            if user:
                to_addr.append(user.email)
            user = c_task_user.query.filter(
                c_task_user.user_name == all_results.log_by).first()
            if user:
                to_addr.append(user.email)

            sendEmail(receivers=to_addr, subject=title,
                      content=content, sender='task@leadrive.com')

        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


@bp.route('/')
@flask_login.login_required
def defaultPage():
    display_name = flask_login.current_user.displayName
    return render_template('/task/task_search.html', display_name=display_name)


@bp.route("/search")
@flask_login.login_required
def task_search():
    display_name = flask_login.current_user.displayName
    return render_template('/task/task_search.html', display_name=display_name)


@bp.route("/create")
@flask_login.login_required
def task_create():
    display_name = flask_login.current_user.displayName
    return render_template('/task/task_new.html', display_name=display_name)


@bp.route("/<task_id>")
@flask_login.login_required
def task_view(task_id):
    display_name = flask_login.current_user.displayName
    id1 = task_id.upper()
    return render_template('/task/task_view.html', task_id=id1, display_name=display_name)

# return the project & department the user can access


@bp.route("/role/get", methods=['POST'])
@flask_login.login_required
def task_role_get():

    property1 = request.form.get('property')
    user_name = flask_login.current_user.displayName
    all_results = c_task_role.query.filter(c_task_role.user_name == user_name, c_task_role.property == property1)\
        .all()

    if all_results:
        result_json = '['
        for i in all_results:
            result_json = result_json + '{' + '"setting":"' + i.value + '"},'
        status = '200'
        value_msg = 'get successfully!'
        result_json = result_json[0:len(result_json) - 1]
        result_json = result_json + ']'
    else:
        status = '401'
        value_msg = 'No Result Found!'
        result_json = '"No Data!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result


# return the config
# now only return the task_type of each project & department
@bp.route("/config/get", methods=['POST'])
def task_config_get():
    property1 = request.form.get('property')
    all_results = c_task_config.query.filter(
        c_task_config.property == property1).all()

    if all_results:
        result_json = '['
        for i in all_results:
            result_json = result_json + '{' + '"setting":"' + i.setting + '"},'
        status = '200'
        value_msg = 'get successfully!'
        result_json = result_json[0:len(result_json) - 1]
        result_json = result_json + ']'
    else:
        status = '401'
        value_msg = 'No Result Found!'
        result_json = '"No Data!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result


# create the new task
@bp.route("/list/new", methods=['POST'])
def task_list_new():
    if flask_login.current_user.displayName:  # if log in
        task_name = request.form.get('task_name')
        pj_dpt = request.form.get('pj_dpt')
        task_type = request.form.get('task_type')
        priority = request.form.get('priority')
        owner = request.form.get('owner')
        description = request.form.get('description')
        task_status = '1-新建'

        user_name = flask_login.current_user.displayName
        # check if can access the resource
        valid = is_access(user_name, 'pj_dpt', pj_dpt)
        if valid == 1:
            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_time = ''
            task_id = 'TK' + time.strftime("%y", time.localtime())
            return_id = c_task_list.query.filter(c_task_list.task_id.like(task_id + '%'))\
                .order_by(c_task_list.task_id.desc()).first()
            if return_id:
                print(return_id.task_id)
                last_id = return_id.task_id
                last_id = last_id[2:8]
                task_id = 'TK' + str(int(last_id) + 1)
            else:
                task_id = task_id + '0001'

            record = c_task_list(task_id=task_id, task_name=task_name, pj_dpt=pj_dpt, task_type=task_type,
                                 priority=priority, owner=owner, description=description, task_status=task_status,
                                 log_by=user_name, log_time=log_time, update_time=update_time)
            db.session.add(record)
            db.session.commit()

            # email to inform the related people
            email_title = '新建任务---' + task_id + ': ' + task_name
            email_content = '<table border="1" cellpadding="0" cellspacing="0"><tr style="background-color: bbb">' \
                '<th style="width:100px">属性</th><th style="width:300px">内容</th></tr>' \
                '<tr><td>任务号</td><td>' + task_id + '</td></tr>' \
                '<tr><td>任务名</td><td>' + task_name + '</td></tr>' \
                '<tr><td>任务描述</td><td>' + description + '</td></tr>' \
                '<tr><td>项目或部门</td><td>' + pj_dpt + '</td></tr>' \
                '<tr><td>任务类型</td><td>' + task_type + '</td></tr>' \
                '<tr><td>优先级</td><td>' + priority + '</td></tr>' \
                '<tr><td>负责人</td><td>' + owner + '</td></tr>' \
                '<tr><td>创建人</td><td>' + user_name + '</td></tr>' \
                '<tr><td>任务状态</td><td>' + task_status + '</td></tr></table>'
            send_email(email_title, task_id, email_content)

            status = '200'
            value_msg = 'Create successfully!'
            result_json = '[{"task_id":"' + task_id + '", "task_name":"' + task_name + '", "task_type":"' + task_type \
                          + '", "description":"' + description + '", "pj_dpt":"' + pj_dpt \
                          + '", "priority":"' + priority + '", "owner":"' + owner \
                          + '", "task_status":"' + task_status + '", "log_time":"' + str(log_time) \
                          + '", "log_by":"' + user_name + '", "update_time":"' + update_time + '"}]'
        else:
            status = '403'
            value_msg = 'Access Deny!'
            result_json = '"Access Deny"'
    else:
        status = '401'
        value_msg = 'Please log in first!'
        result_json = '"Please log in first!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result

# return the task list front end search


@bp.route("/list/search", methods=['POST'])
def task_list_search():
    task_start_id = request.form.get('start_id')
    task_end_id = request.form.get('end_id')
    pj_dpt = request.form.get('pj_dpt')
    task_type = request.form.get('task_type')
    priority = request.form.get('priority')
    owner = request.form.get('owner')
    task_status = request.form.get('task_status')

    user_name = flask_login.current_user.displayName
    # check if can access the resource
    valid = is_access(user_name, 'pj_dpt', pj_dpt)
    if valid == 1:
        filters = {
            c_task_list.task_id.between(task_start_id, task_end_id),
            c_task_list.pj_dpt == pj_dpt
        }

        if task_type != '不限':
            filters.add(c_task_list.task_type == task_type)

        if priority != '不限':
            filters.add(c_task_list.priority == priority)

        if owner != '不限':
            filters.add(c_task_list.owner == owner)

        if task_status != '不限':
            filters.add(c_task_list.task_status == task_status)

        all_results = c_task_list.query.filter(*filters).all()

        if all_results:
            result_json = '['
            for i in all_results:
                last_update = '无更新记录！'
                aaa = c_task_content.query.filter(
                    c_task_content.task_id == i.task_id).all()
                if aaa:
                    last_update = aaa[-1].content
                result_json = result_json + '{' + '"task_id":"' + i.task_id\
                                                + '","task_name":"' + i.task_name\
                                                + '","pj_dpt":"' + i.pj_dpt\
                                                + '","task_type":"' + i.task_type\
                                                + '", "priority":"' + i.priority\
                                                + '", "owner":"' + i.owner\
                                                + '", "task_status":"' + i.task_status\
                                                + '", "last_update":"' + last_update\
                                                + '", "update_time":"' + i.update_time\
                                                + '", "log_by":"' + i.log_by\
                                                + '", "log_time":"' + i.log_time + '"},'
            status = '200'
            value_msg = 'Search successfully!'
            result_json = result_json[0:len(result_json) - 1]
            result_json = result_json + ']'
        else:
            status = '404'
            value_msg = 'No Result Found!'
            result_json = '"No Data!"'
    else:
        status = '403'
        value_msg = 'Access deny!'
        result_json = '"Access Deny!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result

# return the detailed task info of the task
#   1) task property such as task name, description, priority, owner
#   2) task updates
#   3) task property change history


@bp.route("/info/get", methods=['POST'])
def task_info_get():
    task_id = request.form.get('task_id')
    all_results = c_task_list.query.filter(
        c_task_list.task_id == task_id).first()

    if all_results:
        i = all_results
        user_name = flask_login.current_user.displayName
        valid = is_access(user_name, 'pj_dpt', i.pj_dpt)  # check if can access
        if valid == 1:
            #   1) task property such as task name, description, priority, owner
            result_json = '{' + '"task_id":"' + i.task_id\
                + '","task_name":"' + i.task_name\
                + '","pj_dpt":"' + i.pj_dpt\
                + '","task_type":"' + i.task_type\
                + '", "priority":"' + i.priority\
                + '", "owner":"' + i.owner \
                + '", "description":"' + i.description \
                + '", "task_status":"' + i.task_status\
                + '", "update_time":"' + i.update_time\
                + '", "log_by":"' + i.log_by\
                + '", "log_time":"' + i.log_time + '",'

            # 2) task updates
            all_results = c_task_content.query.filter(
                c_task_content.task_id == task_id).all()
            if all_results:
                result_json = result_json + '"content_valid":"True",'
                result_json = result_json + '"content":['
                for i in all_results:
                    time_consume = str(round(i.time_consume, 1))
                    result_json = result_json + '{' + '"task_id":"' + i.task_id \
                        + '","task_seq":' + str(i.task_seq) \
                        + ' ,"update_name":"' + i.update_name \
                        + '","update_time":"' + i.update_time \
                        + '", "time_consume":' + time_consume \
                        + ' , "task_status":"' + i.task_status \
                        + '", "content":"' + i.content \
                        + '", "file_qty":' + str(i.file_qty) + '},'

                result_json = result_json[0:len(result_json) - 1]
                result_json = result_json + '],'
            else:
                result_json = result_json + '"content_valid":"False",'

            #   3) task property change history
            all_results = c_task_log.query.filter(
                c_task_log.task_id == task_id).all()
            if all_results:
                result_json = result_json + '"log_valid":"True",'
                result_json = result_json + '"log":['
                for i in all_results:
                    result_json = result_json + '{' + '"task_id":"' + i.task_id \
                        + '","property":"' + i.property \
                        + '","old_p":"' + i.old \
                        + '","new_p":"' + i.new \
                        + '", "name":"' + i.name \
                        + '", "change_time":"' + i.change_time + '"},'
                result_json = result_json[0:len(result_json) - 1]
                result_json = result_json + ']'
                result_json = result_json + '}'
            else:
                result_json = result_json + '"log_valid":"False"}'

            status = '200'
            value_msg = 'Get successfully!'

        else:
            status = '403'
            value_msg = 'Access Deny!'
            result_json = '"Access Deny!"'
    else:
        status = '404'
        value_msg = 'No Result Found!'
        result_json = '"No Data!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result

# update the task property to the database
# such as description, project & department, prioroty, owner


@bp.route("/info/update", methods=['POST'])
def task_info_update():
    task_id = request.form.get('task_id')
    description = request.form.get('description')
    pj_dpt = request.form.get('pj_dpt')
    task_type = request.form.get('task_type')
    priority = request.form.get('priority')
    owner = request.form.get('owner')

    all_results = c_task_list.query.filter(
        c_task_list.task_id == task_id).first()

    user_name = flask_login.current_user.displayName
    valid = is_access(user_name, 'pj_dpt', pj_dpt)  # check if can access
    if valid == 1:
        change_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        count = 0
        if all_results:
            old_pj_dpt = all_results.pj_dpt
            old_type = all_results.task_type
            old_priority = all_results.priority
            old_owner = all_results.owner

            if all_results.description != description:
                all_results.description = description
                count = 1

            if old_pj_dpt != pj_dpt:
                all_results.pj_dpt = pj_dpt
                count = 1

            if old_type != task_type:
                all_results.task_type = task_type
                count = 1

            if old_priority != priority:
                all_results.priority = priority
                count = 1

            if old_owner != owner:
                all_results.owner = owner
                count = 1

            if count == 1:
                db.session.commit()
                status = '200'
                value_msg = 'Change successfully!'
                result_json = '"Change successfully!"'
            else:
                status = '410'
                value_msg = 'No need to update!'
                result_json = '"No need to update!"'

            if old_pj_dpt != pj_dpt:
                record = c_task_log(task_id=task_id, property='项目或部门', old=old_pj_dpt, new=pj_dpt,
                                    name=user_name, change_time=change_time)
                db.session.add(record)
                db.session.commit()

            if old_type != task_type:
                record = c_task_log(task_id=task_id, property='任务类型', old=old_type, new=task_type,
                                    name=user_name, change_time=change_time)
                db.session.add(record)
                db.session.commit()

            if old_priority != priority:
                record = c_task_log(task_id=task_id, property='优先级', old=old_priority, new=priority,
                                    name=user_name, change_time=change_time)
                db.session.add(record)
                db.session.commit()

            if old_owner != owner:
                record = c_task_log(task_id=task_id, property='负责人', old=old_owner, new=owner,
                                    name=user_name, change_time=change_time)
                db.session.add(record)
                db.session.commit()

                email_title = '任务负责人变更---' + task_id + ': ' + all_results.task_name
                email_content = '<table border="1" cellpadding="0" cellspacing="0"><tr style="background-color: bbb">' \
                    '<th style="width:100px">属性</th><th style="width:300px">内容</th></tr>' \
                    '<tr><td>任务号</td><td>' + task_id + '</td></tr>' \
                    '<tr><td>任务名</td><td>' + all_results.task_name + '</td></tr>' \
                    '<tr><td>任务描述</td><td>' + all_results.description + '</td></tr>' \
                    '<tr><td>项目或部门</td><td>' + all_results.pj_dpt + '</td></tr>' \
                    '<tr><td>任务类型</td><td>' + all_results.task_type + '</td></tr>' \
                    '<tr><td>优先级</td><td>' + all_results.priority + '</td></tr>' \
                    '<tr><td>任务状态</td><td>' + all_results.task_status + '</td></tr>' \
                    '<tr><td>新负责人</td><td>' + owner + '</td></tr></table>'
                send_email(email_title, task_id, email_content)
        else:
            status = '404'
            value_msg = 'No Result Found!'
            result_json = '"No Data!"'
    else:
        status = '403'
        value_msg = 'Access Deny!'
        result_json = '"Access Deny!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result

# update the task status
# total had 6 status: 1-新建，2-进行中，3-待评审，4-暂停，5-关闭，6-完成


@bp.route("/status/change", methods=['POST'])
def task_status_change():
    task_id = request.form.get('task_id')
    new_status = request.form.get('task_status')

    all_results = c_task_list.query.filter(
        c_task_list.task_id == task_id).first()

    user_name = flask_login.current_user.displayName
    # check if can access
    valid = is_access(user_name, 'pj_dpt', all_results.pj_dpt)
    if valid == 1:
        count = 0
        email = 0
        task_name = all_results.task_name
        if all_results:
            old_status = all_results.task_status

            if old_status != '2-进行中' and new_status == '2-进行中':
                count = 1
            if old_status == '2-进行中' and (new_status == '3-待评审' or new_status == '4-暂停'):
                count = 1
                email = 1
            if old_status == '3-待评审' and (new_status == '4-暂停' or new_status == '6-完成'):
                count = 1
                email = 1
            if old_status == '4-暂停' and new_status == '5-终止':
                count = 1
                email = 1

            if count == 1:
                all_results.task_status = new_status
                db.session.commit()

                change_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                record = c_task_log(task_id=task_id, property='任务状态', old=old_status, new=new_status,
                                    name=user_name, change_time=change_time)
                db.session.add(record)
                db.session.commit()
                status = '200'
                value_msg = 'Change successfully!'
                result_json = '{"task_id":"' + task_id + \
                    '","task_status":"' + new_status + '"}'
            else:
                status = '404'
                value_msg = 'No need to update!'
                result_json = '"No need to update!"'

            if email == 1:
                email_title = '任务状态变化---' + task_id + ': ' + task_name
                email_content = '<table border="1" cellpadding="0" cellspacing="0"><tr style="background-color: bbb">' \
                                '<th style="width:100px">属性</th><th style="width:300px">内容</th></tr>' \
                                '<tr><td>任务号</td><td>' + task_id + '</td></tr>' \
                                '<tr><td>任务名</td><td>' + task_name + '</td></tr>' \
                                '<tr><td>任务描述</td><td>' + all_results.description + '</td></tr>' \
                                '<tr><td>负责人</td><td>' + all_results.owner + '</td></tr>' \
                                '<tr><td>更新人</td><td>' + user_name + '</td></tr>' \
                                '<tr><td>新任务状态</td><td>' + new_status + '</td></tr></table>'
                send_email(email_title, task_id, email_content)

        else:
            status = '404'
            value_msg = 'No Result Found!'
            result_json = '"No Data!"'
    else:
        status = '403'
        value_msg = 'Access Deny!'
        result_json = '"Access Deny!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result

# record the task content update


@bp.route("/content/update", methods=['POST'])
def task_content_update():
    task_id = request.form.get('task_id')
    time_consume = request.form.get('task_time')
    input_content = request.form.get('input_content')
    change_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_results = c_task_list.query.filter(
        c_task_list.task_id == task_id).first()

    user_name = flask_login.current_user.displayName
    # check if can access
    valid = is_access(user_name, 'pj_dpt', all_results.pj_dpt)
    if valid == 1:
        if all_results:
            task_status = all_results.task_status
            task_name = all_results.task_name
            description = all_results.description
            owner = all_results.owner

            all_results.update_time = change_time
            db.session.commit()

            all_results = c_task_content.query.filter(c_task_content.task_id == task_id)\
                .order_by(c_task_content.task_seq.desc()).all()
            if all_results:
                task_seq = all_results[0].task_seq + 1
            else:
                task_seq = 1

            record = c_task_content(task_id=task_id, task_seq=task_seq, time_consume=time_consume,
                                    content=input_content, task_status=task_status, file_qty=0,
                                    update_name=user_name, update_time=change_time)
            db.session.add(record)
            db.session.commit()

            email_title = '任务更新---' + task_id + ': ' + task_name
            email_content = '<table border="1" cellpadding="0" cellspacing="0"><tr style="background-color: bbb">' \
                            '<th style="width:100px">属性</th><th style="width:300px">内容</th></tr>' \
                            '<tr><td>任务号</td><td>' + task_id + '</td></tr>' \
                            '<tr><td>任务名</td><td>' + task_name + '</td></tr>' \
                            '<tr><td>任务描述</td><td>' + description + '</td></tr>' \
                            '<tr><td>负责人</td><td>' + owner + '</td></tr>' \
                            '<tr><td>更新人</td><td>' + user_name + '</td></tr>' \
                            '<tr><td>更新内容</td><td>' + input_content + '</td></tr></table>'
            send_email(email_title, task_id, email_content)

            status = '200'
            value_msg = 'Change successfully!'
            result_json = '{"task_id":"' + task_id + '","task_seq":' + str(task_seq) + ' ,"task_time":' \
                          + str(time_consume) + ',"name":"' + user_name + '","update_time":"' \
                          + change_time + '","content":"' + input_content + '"}'
        else:
            status = '404'
            value_msg = 'Task ID is wrong!'
            result_json = '"No Task Record!"'
    else:
        status = '403'
        value_msg = 'Access Deny!'
        result_json = '"Access Deny!"'

    result = '{"status":' + status + ',"msg":"' + \
        value_msg + '","result":' + result_json + '}'
    print(result)
    return result
