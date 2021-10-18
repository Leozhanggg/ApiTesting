# -*- coding:utf-8 -*-
# @Time    : 2021/1/8
# @Author  : Leo Zhang
# @File    : readRelevance.py
# ****************************
import logging
import re

# __relevance = ""
__relevance = []


def get_value(data, value):
    """获取数据中的值

    :param data:
    :param value:
    :return:
    """
    global __relevance
    if isinstance(data, dict):
        # if value in data:
        #     __relevance = data[value]
        # else:
        #     for key in data:
        #         __relevance = get_value(data[key], value)
        for key in data:
            if isinstance(data[key], dict):
                get_value(data[key], value)
            elif isinstance(data[key], list):
                for each in data[key]:
                    if isinstance(each, dict):
                        get_value(each, value)
                # for each in data[key]:
                #     if isinstance(each, dict):
                #         break
                else:
                    if key == value:
                        __relevance.append(data[key])
            else:
                if key == value:
                    __relevance.append(data[key])
    elif isinstance(data, list):
        for key in data:
            if isinstance(key, dict):
                # __relevance = get_value(key, value)
                # break
                get_value(key, value)
    return __relevance


def get_relevance(data, relevance_list, relevance=None):
    """获取关联键值对

    :param data:
    :param relevance_list:
    :param relevance:
    :return:
    """
    global __relevance
    # 获取关联键列表
    relevance_list = re.findall(r"\${(.*?)}", str(relevance_list))

    # 去除参数[n]标识
    for index, value in enumerate(relevance_list):
        mark = re.findall(r"\[\-?[0-9]*\]",  value)
        # if mark:
        #     relevance_list[index] = value.strip(mark[0])
        for m in mark:
            value = value.replace(m, '')
        relevance_list[index] = value

    # 去除重复参数
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
        # 只考虑一个关联键一个值
        # if each in relevance:
        #     pass
        # else:
        #     # 从结果中提取关联键的值
        #     relevance[each] = get_value(data, each)

        # 考虑到一个关联键多个值
        relevance_value = get_value(data, each)
        if relevance_value:
            if each in relevance:
                tmp = relevance[each]
                if isinstance(tmp, list):
                    tmp += relevance_value
                    relevance[each] = tmp
                else:
                    tmp2 = relevance_value.insert(0, tmp)
                    relevance[each] = tmp2
            else:
                relevance[each] = relevance_value
        __relevance = []
    logging.debug("提取关联键对象:\n%s" % relevance)
    return relevance
