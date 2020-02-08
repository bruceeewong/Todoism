# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: __init__.py
    @time: 2020/2/8
    @desc: 
"""
from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)

CORS(api_v1)  # 设置 CORS 避免前端出现跨域问题