# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: __init__.py
    @time: 2020/2/8
    @desc: 
"""
import os
import click

from flask import Flask, request, jsonify, render_template
from flask_login import current_user

from todoism.apis.v1 import api_v1
from todoism.blueprints.auth import auth_bp
from todoism.blueprints.home import home_bp
from todoism.blueprints.todo import todo_bp
from todoism.extensions import db, login_manager, csrf
from todoism.settings import config
from todoism.models import User, Item  # 引用模型类, 数据库才会在create_all时自动生成表


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    # register_template_context(app)

    return app


# 注册扩展程序
def register_extensions(app):
    db.init_app(app)  # SQLAlchemy
    login_manager.init_app(app)  # flask_login LoginManager 实例
    csrf.init_app(app)  # flask_wtf.csrf CSRFProtect实例
    csrf.exempt(api_v1)  # TODO: 为什么要api接口不需要csrf防护


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(api_v1, url_prefix='/v1', subdomain='api')  # enable subdomain support


# 注册template上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            active_items = Item.query.with_parent(current_user).filter_by(done=False).count()
        else:
            active_items = None
        return dict(active_items=active_items)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors.html', code=400, info='Bad Request'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors.html', code=403, info='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        # contentType为 application/json 时, 返回 404 json数据
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html or \
                request.path.startswith('/api'):
            response = jsonify(code=404, message='The requested URL was not found on the server.')
            response.status_code = 404
            return response
        # contentType为其他时, 返回 404 html页面
        return render_template('errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html or \
                request.path.startswith('/api'):
            response = jsonify(code=500, message='An internal server error occurred.')
            response.status_code = 500
            return response
        return render_template('errors.html', code=500, info='Server Error'), 500


# 注册 flask 指令
def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create db after drop')
    def initdb(drop):
        """Initialize the database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Intialized database.')
