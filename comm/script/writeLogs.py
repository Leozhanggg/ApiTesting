# -*- coding:utf-8 -*-
# @Time    : 2020/9/22
# @Author  : Leo Zhang
# @File    : writeLogs.py
# ************************
import logging
import time
import sys
import os


class MyLogs:

    def __init__(self, log_path):
        # 定义日志默认路径和日志名称
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        runtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        logfile = os.path.join(log_path, runtime+'.log')
        logfile_err = os.path.join(log_path, runtime+'_error.log')

        # 第一步，初始化日志对象并设置日志等级
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.handlers = []

        # 第二步，创建一个handler，用于写入debug日志文件
        fh = logging.FileHandler(logfile, mode='a+')
        fh.setLevel(logging.DEBUG)

        # 第三步，创建一个handler，用于写入error日志文件
        fh_err = logging.FileHandler(logfile_err, mode='a+')
        fh_err.setLevel(logging.ERROR)

        # 第四步，再创建一个handler，用于输出info日志到控制台
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)

        # 第五步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        fh_err.setFormatter(formatter)
        sh.setFormatter(formatter)

        # 第六步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(fh_err)
        logger.addHandler(sh)
