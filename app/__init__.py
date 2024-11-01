from flask import Flask
from .blueprints import auth_bp, file_bp, main_bp, plot_bp
from .extensions import db, login_manager, migrate
import click

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app) #登录管理器，注册了flask-login能正常工作，load_user这种自动调用.
    migrate.init_app(app, db)
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(file_bp, url_prefix='/file')
    app.register_blueprint(main_bp, url_prefix='')
    app.register_blueprint(plot_bp, url_prefix='/plot')

    # 注册命令
    from app.models import User
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='create after drop')
    def initdb(drop):
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('数据库已初始化')

    return app