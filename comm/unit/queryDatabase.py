# -*- coding:utf-8 -*-
# @Time    : 2021/03/09
# @Author  : Leo Zhang
# @File    : queryDatabase.py
# **************************
from comm.utils.readYaml import read_yaml_data
from config import DB_CONFIG, PROJECT_NAME
from comm.db import *
import logging
import time
import re

dbcfg = read_yaml_data(DB_CONFIG)[PROJECT_NAME]


def query_mysql(sql):
    """查询MySQL数据

    :param sql: sql查询语句
    :return:
    """
    # 获取配置信息
    timeout = dbcfg['timeout']
    address = dbcfg['mysql_info']['address']
    user = dbcfg['mysql_info']['user']
    auth = dbcfg['mysql_info']['auth']
    db = dbcfg['mysql_info']['db']
    # 初始化MySQL
    host, port = address.split(':')
    mysql = MysqlServer(host, int(port), db, user, auth)
    logging.info('执行查询>>> {}'.format(sql))
    # 循环查询
    for i in range(int(timeout)):
        try:
            result = mysql.query(sql, is_dict=True)
            mysql.close()
            if result:
                return result
            else:
                time.sleep(1)
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))
    else:
        return []


def query_hbase(sql):
    """查询HBase数据

    :param sql: sql查询语句
    :return:
    """
    # 获取配置信息
    timeout = dbcfg['timeout']
    address = dbcfg['hbase_info']['address']
    db = dbcfg['hbase_info']['db']
    # 检索SQL语句
    exp = r"^select .*? from (.*?) where .*?$"
    table = re.findall(exp, sql.strip())[0]
    # 添加数据库
    if '.' not in table:
        sql = sql.strip().replace(table, db+'.'+table)
    # 初始化HBase
    hbase = PhoenixServer(address)
    logging.info('执行查询>>> {}'.format(sql))
    # 循环查询
    for i in range(int(timeout)):
        try:
            result = hbase.query(sql, is_dict=True)
            if result:
                return result
            else:
                time.sleep(1)
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))
    else:
        return []


def query_es(sql):
    """查询ES数据

    :param sql: sql查询语句
    :return:
    """
    # 获取配置信息
    timeout = dbcfg['timeout']
    address = dbcfg['es_info']['address']
    db = dbcfg['es_info']['db']
    logging.info('执行查询>>> {}'.format(sql))
    # 循环查询
    for i in range(int(timeout)):
        try:
            result = elastic_search(address, db, sql)
            if result:
                return result
            else:
                time.sleep(1)
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))
    else:
        return []


def query_solr(sql):
    """查询solr数据

    :param sql: sql查询语句
    :return:
    """
    # 获取配置信息
    timeout = dbcfg['timeout']
    address = dbcfg['solr_info']['address']
    logging.info('执行查询>>> {}'.format(sql))
    # 循环查询
    for i in range(int(timeout)):
        try:
            result = search_solr(address, sql)
            if result:
                return result
            else:
                time.sleep(1)
        except Exception as e:
            raise Exception('查询异常>>> {}'.format(e))
    else:
        return []
