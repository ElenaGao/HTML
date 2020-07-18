#! /usr/bin/python3
# coding:utf-8

"""
@version: 3.8
@author: elena
@file: start.py
@date: 2020/7/18
"""

import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)

from core import src

if __name__ == '__main__':
    src.run()
