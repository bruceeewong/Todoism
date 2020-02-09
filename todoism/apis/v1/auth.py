# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: auth.py
    @time: 2020/2/9
    @desc: 
"""
from functools import wraps

from flask import request


def get_token():
    # Flask/Werkzeug 不识别任何 authentication 类型
    # 所以我们手动解析 header
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)  # TODO: what is this
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
