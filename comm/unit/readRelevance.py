# -*- coding:utf-8 -*-
# @Time    : 2021/1/8
# @Author  : Leo Zhang
# @File    : readRelevance.py
# ****************************
import logging
import re

__relevance = ""


def get_value(data, value):
    """获取数据中的值

    :param data:
    :param value:
    :return:
    """
    global __relevance
    if isinstance(data, dict):
        if value in data:
            __relevance = data[value]
        else:
            for key in data:
                __relevance = get_value(data[key], value)
    elif isinstance(data, list):
        for key in data:
            if isinstance(key, dict):
                __relevance = get_value(key, value)
                break
    return __relevance


def get_relevance(data, relevance_list, relevance=None):
    """获取关联键值对

    :param data:
    :param relevance_list:
    :param relevance:
    :return:
    """
    # 获取关联键列表
    relevance_list = re.findall(r"\${(.*?)}", str(relevance_list))
    relevance_list = list(set(relevance_list))
    logging.debug("获取关联键列表:\n%s" % relevance_list)
    # 判断关联键和源数据是否有值
    if (not data) or (not relevance_list):
        return relevance

    # 判断是否存在其他关联键对象
    if not relevance:
        relevance = dict()
    # 遍历关联键
    for each in relevance_list:
        if each in relevance:
            pass
            # # 考虑到一个关联键，多个值
            # if isinstance(relevance[each], list):
            #     a = relevance[each]
            #     a.append(relevance_value)
            #     relevance[each] = a
            # else:
            #     a = relevance[each]
            #     b = list()
            #     b.append(a)
            #     b.append(relevance_value)
            #     relevance[each] = b
        else:
            # 从结果中提取关联键的值
            relevance[each] = get_value(data, each)
    logging.debug("提取关联键对象:\n%s" % relevance)
    return relevance



