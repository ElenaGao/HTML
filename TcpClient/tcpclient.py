#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: tcpclient.py
@date: 2020/7/18
"""
import socket


def get_client():
    client = socket.socket()
    client.connect(('127.0.0.1', 8080))
    return client
