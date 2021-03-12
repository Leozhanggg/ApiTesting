# -*- coding:utf-8 -*-
# @Time    : 2021/03/09
# @Author  : Leo Zhang
# @File    : queryMysql.py
# **************************
import pymysql
import logging


class MysqlServer:
    """
    封装MySQL常用方法。
    """
    def __init__(self, host, port, db, user, passwd, charset='utf8'):
        # 初始化数据库
        logging.debug('Connect MySQL: host={host}, port={port}, db={db}, user={user}, passwd={passwd}'
                      .format(host=host, port=port, db=db, user=user, passwd=passwd))
        try:
            self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        except Exception as e:
            raise Exception('连接异常>>> {}'.format(e))

    # 增加、修改、删除命令语句
    def execute(self, sql):
        try:
            # 创建游标
            cur = self.conn.cursor(cursor=pymysql.cursors.Cursor)
            # 执行sql语句
            cur.execute(sql)
            # 提交事务
            self.conn.commit()
            # 关闭游标
            cur.close()
        except Exception as e:
            # 出错时回滚
            self.conn.rollback()
            raise Exception('执行异常>>> {}'.format(e))

    # 查询所有数据,多个值
    def query(self, sql, is_dict):
        try:
            # 检查当前连接是否已关闭并进行重接
            self.conn.ping(reconnect=True)
            # 判断是否需要返回结果为字典类型
            if is_dict:
                cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            else:
                cur = self.conn.cursor(cursor=pymysql.cursors.Cursor)
            # 执行sql语句
            cur.execute(sql)
            # 查询结果
            data = cur.fetchall()
            # 关闭游标
            cur.close()
            return data
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))

    # 关闭数据库连接
    def close(self):
        self.conn.close()
