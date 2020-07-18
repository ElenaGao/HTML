#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: admin.py
@date: 2020/7/18
"""

from TcpClient import tcpclient
from lib import common
import os
from conf import settings

user_dic = {
    'session': None
}


def register(client):
    while True:
        name = input('please input your username:>>>').strip()
        password = input('please input your password:>>>').strip()
        confirm_password = input('please confirm your password:>>>').strip()
        if password == confirm_password:
            send_dict = {'type': 'register',
                         'name': name,
                         'password': common.get_md5(password),
                         'user_type': 'admin'
                         }
            back_dict = common.send_back(client, send_dict)
            if back_dict.get('flag'):
                print(back_dict['msg'])
                break
            else:
                print(back_dict['msg'])
        else:
            print('两次密码不一样')


def login(client):
    while True:
        name = input('please input your username:>>>').strip()
        password = input('please input your password:>>>').strip()
        send_dict = {'type': 'register',
                     'name': name,
                     'password': common.get_md5(password),
                     'user_type': 'admin'
                     }
        back_dict = common.send_back(client, send_dict)
        if back_dict.get('flag'):
            user_dic['session'] = back_dict['session']
            print(back_dict['msg'])
            break
        else:
            print(back_dict['msg'])


def upload_movie(client):
    pass


def delete_movie(client):
    pass


def release_notice(client):
    pass


func_dict = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_movie,
    '5': release_notice
}


def admin_view():
    client = tcpclient.get_client()
    while True:
        print("""
            1. 注册
            2. 登录
            3. 上传视频
            4. 删除视频
            5. 发布公告
        """)
        choice = input('please choice:>>>').strip()
        if choice not in func_dict: continue
        func_dict.get(choice)(client)
