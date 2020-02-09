# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: resources.py
    @time: 2020/2/8
    @desc: 
"""
from flask import jsonify, g, request, current_app, url_for
from flask.views import MethodView

from todoism.extensions import db
from todoism.apis.v1 import api_v1

# 入口API /
from todoism.apis.v1.auth import auth_required, generate_token
from todoism.apis.v1.errors import api_abort, ValidationError
from todoism.apis.v1.schemas import item_schema, user_schema, items_schema
from todoism.models import Item, User


class IndexAPI(MethodView):

    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://todoism.bruski.wang/api/v1",
            "current_user_url": "http://todoism.bruski.wang/api/v1/user",
            "authentication_url": "http://todoism.bruski.wang/api/v1/token",
            "item_url": "http://todoism.bruski.wang/api/v1/items/{item_id}",
            "current_user_items_url": "http://todoism.bruski.wang/api/v1/user/items/{?page,per_page}",
            "current_user_active_items_url": "http://todoism.bruski.wang/api/v1/user/items/active{?page,per_page}",
            "current_user_completed_items_url": "http://todoism.bruski.wang/api/v1/user/items/completed{?page,per_page}",
        })


# Token相关API
class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)

        response = jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        })
        # 禁止浏览器缓存本次返回的结果
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


# 用户资源相关API
class UserAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        """Get User"""
        return jsonify(user_schema(g.current_user))


# 从request中获取body属性
def get_item_body():
    data = request.get_json()
    body = data.get('body')
    # 如果 body 不存在 或 为空, 抛出参数错误
    if body is None or str(body).strip() == '':
        raise ValidationError('The item body was empty or invalid.')
    return body


# 单个todo目标资源相关API
class ItemAPI(MethodView):
    decorators = [auth_required]

    def get(self, item_id):
        """Get item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        return jsonify(item_schema(item))

    def put(self, item_id):
        """Edit item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        item.body = get_item_body()
        db.session.commit()
        return '', 204

    def patch(self, item_id):
        """Toggle Item"""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        item.done = not item.done
        db.session.commit()
        return '', 204

    def delete(self, item_id):
        """Delete Item"""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        db.session.delete(item)
        db.session.commit()
        return '', 204


# 多个todo目标资源相关API
class ItemsAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        """Get current user's all items"""
        # 获取分页属性
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['TODOISM_ITEM_PER_PAGE']
        pagination = Item.query.with_parent(g.current_user).paginate(page, per_page)

        items = pagination.items
        current = url_for('.items', page=page, _external=True)
        prev = None
        if pagination.has_prev:
            prev = url_for('.item', page=page - 1, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('.items', page=page + 1, _external=True)
        return jsonify(items_schema(items, current, prev, next, pagination))

    def post(self):
        """Create new item"""
        item = Item(body=get_item_body(), author=g.current_user)
        db.session.add(item)
        db.session.commit()

        response = jsonify(item_schema(item))
        response.status_code = 201
        response.headers['Location'] = url_for('.item', item_id=item.id, _external=True)  # 设置该资源的url
        return response


# 注册路由
api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
api_v1.add_url_rule('/user', view_func=UserAPI.as_view('user'), methods=['GET'])
api_v1.add_url_rule('/user/items', view_func=ItemsAPI.as_view('items'), methods=['GET', 'POST'])
api_v1.add_url_rule('/user/items/<int:item_id>', view_func=ItemAPI.as_view('item'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
