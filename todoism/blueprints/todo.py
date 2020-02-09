# -*- coding: utf-8 -*-
"""
    @author: Bruski Wang
    @contact: bruskiwang@outlook.com
    @file: todo.py
    @time: 2020/2/9
    @desc: 
"""
from flask import Blueprint, render_template

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app')
def app():
    return render_template('_app.html')
