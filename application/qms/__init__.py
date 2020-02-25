import flask

bp=flask.Blueprint('qms', __name__, url_prefix='/qms')

@bp.route('/')
def default():
    return 'qms home'

