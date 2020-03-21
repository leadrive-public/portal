import sqlite3
import flask_login
import ldap3
import os
import flask

class User(flask_login.UserMixin):
    pass

def databaseFilePath():
    return os.path.join(flask.current_app.config['DATABASE'], 'user.sqlite3')

def getUserByName(name):
    try:
        # print('Connecting {}...'.format(databaseFilePath()))
        conn=sqlite3.connect(databaseFilePath())
    except:
        print('Fail to connect user database!\n')
        return None
    try:
        cmd='select id, userName, displayName from user where userName="{}"'.format(name)
        # print(cmd)
        c=conn.execute(cmd)
        r=c.fetchone()
        user=User()
        user.id=r[0]
        user.name=r[1]
        user.displayName=r[2]
        conn.close()
        # print('Get user name={}\n'.format(user.displayName))
        return user
    except Exception as e:
        # print('Fail to find user {}\n'.format(name))
        print(e)
        return None
    finally:
        conn.close()
        pass
    pass

def getUserById(id):
    try:
        conn=sqlite3.connect(databaseFilePath())
    except:
        return None
    try:
        c=conn.execute('select id, userName, displayName from user where id={}'.format(id))
        r=c.fetchone()
        user=User()
        user.id=id
        user.name=r[1]
        user.displayName=r[2]
        conn.close()
        # print('Get user name={}\n'.format(user.displayName))
        return user
    except:
        return None
    finally:
        conn.close()

def validate(userName, password):
    server=ldap3.Server(host="192.168.17.30")
    conn=ldap3.Connection(server, user="leadrive\\oa", password="CTC1349sso")
    conn.open()
    conn.bind()
    
    # 查询员工
    res=conn.search(
        search_base="ou=员工,dc=leadrive,dc=com",
        search_filter="(userPrincipalName={})".format(userName),
        search_scope=ldap3.SUBTREE,
        attributes=["displayName", "userPrincipalName", "mail"],
        paged_size=5)
    
    if res:
        entry=conn.response[0]
        dn=entry["dn"]
        attr_dict=entry["attributes"]
        # print(dn)
        try:
            conn2=ldap3.Connection(server, user=dn, password=password)
            conn2.open()
            conn2.bind()
            if (conn2.result["description"]=="success"):
                # print((attr_dict["userPrincipalName"], attr_dict["displayName"]))
                return {'userName': attr_dict["userPrincipalName"], 'displayName': attr_dict["displayName"]}
        except Exception as e:
            print(e)
            pass
        pass
    
    # 查询实习生
    res=conn.search(
        search_base="ou=实习生,dc=leadrive,dc=com",
        search_filter="(userPrincipalName={})".format(userName),
        search_scope=ldap3.SUBTREE,
        attributes=["displayName", "userPrincipalName", "mail"],
        paged_size=5)

    if res:
        entry=conn.response[0]
        dn=entry["dn"]
        attr_dict=entry["attributes"]
        # print(dn)
        try:
            conn2=ldap3.Connection(server, user=dn, password=password)
            conn2.open()
            conn2.bind()
            if (conn2.result["description"]=="success"):
                # print((attr_dict["userPrincipalName"], attr_dict["displayName"]))
                return {'userName': attr_dict["userPrincipalName"], 'displayName': attr_dict["displayName"]}
        except Exception as e:
            pass
        pass
    
    return None

def getUsers():
    users=[]
    try:
        conn = sqlite3.connect(databaseFilePath())
    except Exception as e:
        print(e)
        return None
    try:
        cmd='select id, userName, displayName from user order by userName'
        cursor=conn.execute(cmd)
        for row in cursor:
            user={}
            user['id']=row[0]
            user['name']=row[1]
            user['displayName']=row[2]
            users.append(user)
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()
    return users