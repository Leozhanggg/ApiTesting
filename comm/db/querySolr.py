# -*- coding:utf-8 -*-
# @Time    : 2021/03/12
# @Author  : Leo Zhang
# @File    : querySolr.py
# *************************
import pysolr
import logging
import re


def search_solr(address, sql):
    """获取Solr数据

    :param address: 地址(格式：ip:port)
    :param sql: sql查询语句
    :return:
    """
    # 检索SQL语句
    exp = r"^select (.*?) from (.*?) where (.*?)$"
    res = re.findall(exp, sql.strip())
    fields, db, conditions = res[0]

    # 重新拼接查询条件
    query = ''
    for each in conditions.split(' and '):
        key, value = each.replace('\'', '').replace('\"', '').split('=')
        if query:
            query += '&& '
        query += '{}:"{}" '.format(key, value)

    # 初始化Solr
    try:
        base_url = 'http://{0}/solr/{1}/'.format(address, db)
        solr = pysolr.Solr(base_url)
    except Exception as e:
        raise Exception('连接异常>>> \n{}'.format(e))

    # 执行查询
    query_str = 'GET {0}select?q={1}'.format(base_url, query)
    logging.info('执行查询>>> {}'.format(query_str))
    try:
        data = solr.search(query)
        result = list()
        for each in data:
            result.append(each)
        if result:
            # 判断是否返回全部字段
            if fields == '*':
                return result
            else:
                # 返回指定字段
                result_new = list()
                for res in result:
                    line = dict()
                    for each in fields.split(','):
                        try:
                            line[each] = res[each]
                        except KeyError:
                            raise KeyError('Solr未知字段>>> {}'.format(each))
                    result_new.append(result)
                return result_new
    except Exception as e:
        raise Exception('查询异常>>> \n{}'.format(e))
