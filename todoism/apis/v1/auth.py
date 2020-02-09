# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: auth.py
    @time: 2020/2/9
    @desc: 登录验证模块
"""
from functools import wraps
from flask import request, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, \
    SignatureExpired  # https://pythonhosted.org/itsdangerous/#itsdangerous.Serializer

from todoism.models import User
from todoism.apis.v1.errors import api_abort, token_missing, invalid_token


# 根据app的SECRET_KEY生成token
def generate_token(user):
    expiration = 3600  # 1小时有效期
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


# 验证token
def validate_token(token):
    # 利用Serializer加秘钥去解密传来的token
    # 如果解密后的id能找到user代表没问题, 设置全局的current_user为该user
    # 否则有可能是token被篡改或过期
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False

    user = User.query.get(data['id'])
    if user is None:
        return False

    # 设置全局的current_user为该user!
    g.current_user = user
    return True


# 从请求的headers中获取认证信息
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


# 认证校验装饰器
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated
