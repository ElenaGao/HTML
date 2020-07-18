#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: src.py
@date: 2020/7/18
"""

from core import admin, user

func_dict = {
    '1': admin.admin_view,
    '2': user.user_view,
}


def run():
    while True:
        print("""
       1. 管理员视图
       2. 用户视图
       """)

        choice = input('please choice:>>>>').strip()
        if choice not in func_dict: continue
        func_dict.get(choice)()
