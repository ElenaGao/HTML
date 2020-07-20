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
    while True:
        movie_list = common.get_upload_movie_list()
        if not movie_list:
            print('暂无可上传的影片')
        for i, m in enumerate(movie_list):
            print(f'{i + 1} : {m}')

        choice = input('please choice movie num to upload:>>>').strip()
        if choice == 'q': break
        if choice.isdigit():
            choice = int(choice)
            if choice in range(1, len(movie_list) + 1):
                movie_path = os.path.join(settings.BASE_MOVIE_PATH, movie_list[choice - 1])
                movie_md5 = common.get_file_md5(movie_path)
                # 先用md5去服务端校验是否已有相应视频存在
                send_dic = {'type': 'check_movie', 'session': user_dic['session'], 'file_md5': movie_md5}
                back_dic = common.send_back(client, send_dic)
                if back_dic['flag']:
                    is_free = input('please choice free or not free(y/n)>>>:').strip()
                    is_free = 1 if is_free == 'y' else 0
                    # 文件大小
                    file_size = os.path.getsize(movie_path)
                    send_dic = {'type': 'upload_movie', 'session': user_dic['session'],
                                'file_name': movie_list[choice - 1],
                                'file_size': file_size, 'file_md5': movie_md5, 'is_free': is_free
                                }
                    back_dic = common.send_back(client, send_dic, movie_path)
                    if back_dic['flag']:
                        print(back_dic['msg'])
                        break
                    else:
                        print(back_dic['msg'])
                else:
                    print(back_dic['msg'])
            else:
                print('choice not in range')
        else:
            print('please input number')


def delete_movie(client):
    while True:
        # 先查询出所有没有被删除的电影列表
        send_dic = {"type": 'get_movie_list', 'session': user_dic['session'],
                    'movie_type': 'all'}  # 返回的电影列表可以全部是收费，全部是免费，收费免费都有
        back_dic = common.send_back(client, send_dic)
        if back_dic['flag']:
            movie_list = back_dic.get['movie_list']
            for i, m in enumerate(movie_list):
                print("%s:%s-%s" % (i + 1, m[0], m[1]))
            choice = input('please choice movie number to delete:>>>').strip()
            if choice == 'q': break
            if choice.isdigit():
                choice = int(choice)
                if choice in range(1, len(choice) + 1):
                    send_dic = {'type': 'delete_movie', 'session': user_dic['session'],
                                'delete_movie_id': movie_list[choice - 1][2]}
                    back_dic = common.send_back(client, send_dic)
                    if back_dic['flag']:
                        print(back_dic['msg'])
                        break
                    else:
                        print(back_dic['msg'])
                else:
                    print('choice not in range')
            else:
                print('choice must be a number')
        else:
            print(back_dic['msg'])


def release_notice(client):
    while True:
        title = input('please input notice tilte:>>>>').strip()
        content = input('please input notice content:>>>').strip()
        send_dic = {'type': "release_note", 'title': title, 'content': content, 'session': user_dic['session']}
        back_dic = common.send_back(client, send_dic)
        if back_dic['flag']:
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])


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
