# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruski@qq.com
    @file: __init__.py
    @time: 2020/2/8
    @desc: 
"""
import os

from flask import Flask

from todoism.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])

    return app
