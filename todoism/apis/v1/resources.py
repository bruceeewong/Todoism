# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: resources.py
    @time: 2020/2/8
    @desc: 
"""
from flask import jsonify
from flask.views import MethodView

from todoism.apis.v1 import api_v1


# 入口API /
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


# 注册路由
api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
