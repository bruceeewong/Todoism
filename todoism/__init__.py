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

from flask import Flask

from todoism.apis.v1 import api_v1
from todoism.extensions import db
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

    return app


# 注册扩展程序
def register_extensions(app):
    db.init_app(app)  # SQLAlchemy


# 注册蓝图
def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(api_v1, url_prefix='/v1', subdomain='api')  # enable subdomain support


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
