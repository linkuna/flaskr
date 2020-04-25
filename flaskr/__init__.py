import os
from flask import Flask
from flaskr.database import init_db
from flaskr.config import Config
from flaskr.handle_helper import *


def create_app(test_config=None):
    # from . import db
    from flaskr.api import user, bill, blog, back
    from flaskr.celery_app import cele
    from flaskr.redisutils import RedisConn

    app = Flask(__name__, instance_relative_config=True)
    # app.config['SECRET_KEY'] = 'dev'
    # app.config['SQLALCHEMY_DATABASE_URI'] = ''
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config.from_object(Config)
    # if test_config is None:
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(user.bp)
    app.register_blueprint(blog.bp, url_prefix='/blog')
    app.register_blueprint(back.bp, url_prefix='/back')
    app.register_blueprint(bill.bp, url_prefix='/bill')
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    app.route('/')(blog.index)
    app.before_request(before_request)
    app.after_request(after_request)
    # app.errorhandler(Exception)(error_handle)
    init_db(app)
    RedisConn.init(config.Config.REDIS_HOST, config.Config.REDIS_PORT,
                   config.Config.REDIS_PASSWORD, config.Config.REDIS_DB)

    return app

