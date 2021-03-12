# -*- coding:utf-8 -*-
# @Time    : 2021/03/09
# @Author  : Leo Zhang
# @File    : queryRedis.py
# **************************
import logging
import redis


def exec_redis(address, auth, db_num, db_type, key):
    """获取redis数据

    :param address: 内存库地址(格式：ip:port)
    :param auth: 内存库密码
    :param db_num: 查询内存库号
    :param db_type: 数据库类型
    :param key: 查询key值
    :return:
    """
    # 初始化redis连接
    host, port = address.split(':')
    logging.debug('Redis Info: host={}, port={}, auth={}, db={}, type={}'
                  .format(host, port, auth, db_num, db_type))
    conn = redis.StrictRedis(host=host, port=int(port), db=db_num,
                             password=auth, decode_responses=True)
    logging.info('执行查询>>> db={}, key={}'.format(db_num, key))

    # 获取string类型指定key的对应值
    if 'string' in db_type:
        result = conn.get(key)
    # 获取hash类型指定key的所有数据
    elif 'hash' in db_type:
        result = conn.hgetall(key)
    # 获取zset类型指定key的前50行数据
    elif 'zset' in db_type:
        result = conn.zrange(key, 0, 50, desc=False,
                             withscores=True, score_cast_func=int)
    # 获取set类型指定key的所有数据
    elif 'set' in db_type:
        result = conn.smembers(key)
    # 获取list类型指定key的前10个数据
    elif 'list' in db_type:
        result = conn.lrange(key, 0, 10)
    else:
        raise Exception('未知的数据类型{}，请检查dbinfo配置'.format(db_type))

    logging.info('查询结果>>> {}'.format(result))
    return result
