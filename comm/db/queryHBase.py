# -*- coding:utf-8 -*-
# @Time    : 2021/03/09
# @Author  : Leo Zhang
# @File    : queryHBase.py
# **************************
import phoenixdb
import phoenixdb.cursor
from comm import *
import logging


class PhoenixServer(object):
    """
    封装HBase常用方法。
    """
    def __init__(self, address):
        url = 'http://{}/'.format(address)
        logging.debug('Connect HBase: {}'.format(url))
        try:
            self.conn = phoenixdb.connect(url, autocommit=True)
        except Exception as e:
            raise Exception('连接异常>>> {}'.format(e))

    # 增加、修改、删除命令语句
    def execute(self, sql):
        try:
            # 创建游标
            cursor = self.conn.cursor(cursor_factory=phoenixdb.cursor.Cursor)
            # 执行sql语句
            cursor.execute(sql)
            # 关闭游标
            cursor.close()
        except Exception as e:
            raise Exception('执行异常>>> {}'.format(e))

    # 查询所有数据,多个值
    def query(self, sql, is_dict):
        try:
            # 判断是否需要返回结果为字典类型
            if is_dict:
                cursor = self.conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor)
            else:
                cursor = self.conn.cursor(cursor_factory=phoenixdb.cursor.Cursor)
            # 执行sql语句
            cursor.execute(sql)
            # 查询结果
            data = cursor.fetchall()
            # 关闭游标
            cursor.close()
            return data
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))

    # 关闭数据库连接
    def close(self):
        self.conn.close()
