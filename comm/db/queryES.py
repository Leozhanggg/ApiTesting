# -*- coding:utf-8 -*-
# @Time    : 2021/03/09
# @Author  : Leo Zhang
# @File    : queryES.py
# **************************
import elasticsearch
import logging
import re


def elastic_search(address, db, sql):
    """获取ElasticSearch数据

    :param address: ES地址(格式：ip:port)
    :param db: 索引库名
    :param sql: sql查询语句
    :return:
    """
    # 初始化ES
    try:
        es = elasticsearch.Elasticsearch([address])
    except Exception as e:
        raise Exception('连接异常>>> \n{}'.format(e))

    # 检索SQL语句
    exp = r"^select (.*?) from (.*?) where (.*?)$"
    res = re.findall(exp, sql.strip())
    fields, table, conditions = res[0]
    # 重新拼接查询条件
    query = ''
    for each in conditions.split(' and '):
        key, value = each.replace('\'', '').replace('\"', '').split('=')
        if query:
            query += '&& '
        query += '{}:"{}" '.format(key, value)

    # 执行查询
    db_table = db + '@' + table
    # query_str = 'GET http://{0}/{1}/_search?q={2}'.format(address, db_table, query)
    # logging.info('执行查询>>> {}'.format(query_str))
    try:
        # 查询ES，并截取hits字段
        data = es.search(index=db_table, q=query)
        hits = data['hits']['hits']
        if hits:
            # 截取字段值_source
            new_hits = list()
            for hit in hits:
                new_hits.append(hit['_source'])
            # 判断是否返回全部字段
            if fields == '*':
                return new_hits
            else:
                # 返回指定字段
                source_new = list()
                for hit in new_hits:
                    result = dict()
                    for each in fields.split(','):
                        try:
                            result[each] = hit[each]
                        except KeyError:
                            raise KeyError('ES未知字段>>> {}'.format(each))
                    source_new.append(result)
                return source_new
    except Exception as e:
        raise Exception('查询异常>>> \n{}'.format(e))
