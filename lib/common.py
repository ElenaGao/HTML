#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: common.py
@date: 2020/7/18
"""
import os
import json
import hashlib
import struct
from conf import settings


def send_back(client, send_dict, file=None):
    send_bytes = json.dumps(send_dict).encode('utf-8')
    client.send(struct.pack('i', len(send_bytes)))
    client.send(send_bytes)

    # 传文件
    if file:
        with open(file, 'rb') as f:
            for line in f:
                client.send(line)

    back_header = client.recv(4)
    back_bytes = client.recv(struct.unpack('i', back_header)[0])
    back_dict = json.loads(back_bytes.decode('utf-8'))
    return back_dict


def get_md5(password):
    md = hashlib.md5()
    md.update(password.encode('utf-8'))
    return md.hexdigest()


def get_upload_movie_list():
    movie_list = os.listdir(settings.BASE_MOVIE_PATH)
    return movie_list


def get_file_md5(file_path):
    if os.path.exists(file_path):
        md = hashlib.md5()
        # 切片获取大文件固定几个位置的数据，节省大文件md5值获取时间
        file_size = os.path.getsize(file_path)
        file_list = [0, file_size // 3, (file_size // 3) * 2, file_size - 10]
        with open(file_path, 'rb') as f:
            for line in file_list:
                f.seek(line)
                md.update(f.read(10))
        return md.hexdigest()
