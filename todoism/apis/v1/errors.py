# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: errors.py
    @time: 2020/2/9
    @desc: 发生错误时对应的返回函数
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# 定义HTTP状态码与json格式数据的错误的返回函数
from todoism.apis.v1 import api_v1


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response  # You can also just return (response, code) tuple


# token失效或错误时的返回函数
def invalid_token():
    response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid.')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


# token不存在时的返回函数
def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authenticate'] = 'Bearer'  # TODO: 什么作用?
    return response


class ValidationError(ValueError):
    pass


# 定义api_v1蓝本范围的统一ValidationError错误处理
@api_v1.errorhandler(ValidationError)
def validation_error(e):
    return api_abort(400, e.args[0])
