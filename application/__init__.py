import os
import flask
import flask_login

from . import user as userService
from . import qms
from . import project
from . import etime
from . import ioi
from . import estaffing

def create_app():
    app=flask.Flask(__name__,static_url_path="")
    app.secret_key=os.urandom(24)
    app.config['DATABASE']=os.path.join(os.path.dirname(__file__), 'database')

    loginManager=flask_login.LoginManager()
    loginManager.init_app(app)
    loginManager.login_view='/login'

    @loginManager.user_loader
    def load_user(id):
        user=userService.getUserById(id)
        return user

    app.register_blueprint(qms.bp, url_prefix='/qms')
    app.register_blueprint(project.bp, url_prefix='/project')
    app.register_blueprint(userService.bp, url_prefix='/user')
    app.register_blueprint(etime.bp,  url_prefix='/etime')
    app.register_blueprint(ioi.bp,  url_prefix='/ioi')
    app.register_blueprint(estaffing.bp,  url_prefix='/estaffing')

    # /
    @app.route('/')
    @flask_login.login_required
    def default():
        user=flask_login.current_user
        if user.is_authenticated:
            return flask.render_template("dashboard.html", user=user)
        else:
            return flask.redirect('/login')
        return 'default'

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if flask.request.method=='POST':
            userName=flask.request.form['userName']
            password=flask.request.form['password']
            rememberMe=False
            for key,value in flask.request.form.items():
                if key=='rememberMe':
                    if value=='on':
                        rememberMe=True
                        pass
                    pass
                pass
            ldapUser=userService.validate(userName, password)
            if ldapUser is not None:
                print('User {} validation is OK!'.format(userName))
                user=userService.getUserByName(userName)
                if user is None:
                    return flask.abort(400)
                flask_login.login_user(user, remember =rememberMe)
                flask.flash('Logged in successfully.')
                next = flask.request.form['next']
                return flask.redirect(next or flask.url_for('default'))
            else:
                print('{} login failed!\n'.format(userName))
                return flask.render_template("login.html", loginFail=True)
        else: # GET
            if flask_login.current_user.is_authenticated:
                # print(flask_login.current_user)
                return flask.render_template("login.html")
            else:
                return flask.render_template("login.html")

    @app.route('/logout')
    def logout():
        flask_login.logout_user()
        return flask.redirect('/login')

    return app