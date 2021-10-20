# -*- coding:utf-8 -*-
# @Time    : 2021/2/3
# @Author  : Leo Zhang
# @File    : initializePremise.py
# **************************
import logging
import time
import json
import os
from json import JSONDecodeError
from comm.unit import apiSend, readRelevance, replaceRelevance
from comm.utils import readYaml
API_CONFIG = str(os.path.realpath(__file__)).split('comm')[0] + 'config.yml'


# def save_token(case_data, rsp_data):
#     if case_data['test_info']['address'] == '/api/blade-auth/oauth/token':
#         # 把获取的token保存配置文件中
#         cfg = readYaml.read_yaml_data(API_CONFIG)
#         cfg['headers']['Blade-Auth'] = 'Bearer ' + rsp_data['access_token']
#         readYaml.write_yaml_file(API_CONFIG, cfg)


def read_json(summary, json_obj, case_path):
    """
    校验内容读取
    :param summary: 用例名称
    :param json_obj: json文件或数据对象
    :param case_path: case路径
    :return:
    """
    if not json_obj:
        return json_obj
    elif isinstance(json_obj, dict):
        return json_obj
    else:
        try:
            # 读取json文件指定用例数据
            with open(case_path+'/'+json_obj, "r", encoding="utf-8") as js:
                data_list = json.load(js)
                for data in data_list:
                    if data['summary'] == summary:
                        return data['body']
        except FileNotFoundError:
            raise Exception("用例关联文件不存在\n文件路径： %s" % json_obj)
        except JSONDecodeError:
            raise Exception("用例关联的文件有误\n文件路径： %s" % json_obj)


def prepare_case(pre_case_title, relevance, test_suite):
    """
    调用前置接口并返回响应消息体
    :param pre_case_title: 前置用例
    :param relevance: 关联值对象
    :param test_suite: 用例集
    :return:
    """
    # 获取前置接口用例
    logging.info("获取前置接口测试用例：{}".format(pre_case_title))
    for each in test_suite:
        if each['test_info']['title'] == pre_case_title:
            pre_case_data = each
            break
    else:
        raise Exception("前置接口测试用例不存在：{}".format(pre_case_title))
    pre_test_info = pre_case_data['test_info']
    pre_test_case = pre_case_data['test_case']
    # 判断前置接口是否也存在前置接口
    if pre_test_info["premise"]:
        init_premise(pre_test_info["premise"], relevance, test_suite)

    for i in range(3):
        # 处理前置接口测试信息
        pre_test_info = replaceRelevance.replace(pre_test_info, relevance)
        logging.debug("测试信息处理结果：{}".format(pre_test_info))
        # 处理前置接口入参：获取入参-替换关联值-发送请求
        pre_parameter = replaceRelevance.replace(pre_test_case['parameter'], relevance)
        pre_test_case['parameter'] = pre_parameter
        logging.debug("请求参数处理结果：{}".format(pre_parameter))
        logging.info("执行前置接口测试用例：{}".format(pre_test_info))
        code, data = apiSend.send_request(pre_test_info, pre_test_case)
        # 检查接口是否调用成功
        if data:
            # save_token(pre_case_data, data)
            return data
        else:
            time.sleep(1)
            logging.error("前置接口请求失败！等待1秒后重试！")
    else:
        logging.info("前置接口请求失败！尝试三次失败！")
        raise Exception("获取前置接口关联数据失败！")


def init_premise(test_info, case_data, test_suite):
    """用例前提条件执行，提取关键值

    :param test_info: 测试信息
    :param case_data: 用例数据
    :param test_suite: 用例集
    :return:
    """
    # 获取项目公共关联值
    __relevance = readYaml.read_yaml_data(API_CONFIG)

    # 判断是否存在前置接口
    pre_case_title_list = test_info["premise"].replace(' ', '')
    if pre_case_title_list:
        pre_case_title_list = pre_case_title_list.split(',')
        data = list()
        for pre_case_title in pre_case_title_list:
            each_data = prepare_case(pre_case_title, __relevance, test_suite)
            data.append(each_data)

        # 处理测试信息
        __relevance = readRelevance.get_relevance(data, test_info, __relevance)
        test_info = replaceRelevance.replace(test_info, __relevance)
        logging.debug("测试信息处理结果：{}".format(test_info))

        # 处理当前接口入参：获取入参-获取关联值-替换关联值
        parameter = case_data['parameter']
        __relevance = readRelevance.get_relevance(data, parameter, __relevance)
        parameter = replaceRelevance.replace(parameter, __relevance)
        case_data['parameter'] = parameter
        logging.debug("请求参数处理结果：{}".format(parameter))

        # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
        expected_rs = case_data['check_body']['expected_result']
        # 判断是否存在请求参数
        if parameter:
            msg_body = parameter.copy()
            msg_body['pre_response'] = data
        else:
            msg_body = data
        __relevance = readRelevance.get_relevance(msg_body, expected_rs, __relevance)
        expected_rs = replaceRelevance.replace(expected_rs, __relevance)
        case_data['check_body']['expected_result'] = expected_rs
        logging.debug("期望返回处理结果：{}".format(case_data))

    else:
        # 处理测试信息
        test_info = replaceRelevance.replace(test_info, __relevance)
        logging.debug("测试信息处理结果：{}".format(test_info))

        # 处理当前接口入参：获取入参-获取关联值-替换关联值
        parameter = case_data['parameter']
        parameter = replaceRelevance.replace(parameter, __relevance)
        case_data['parameter'] = parameter
        logging.debug("请求参数处理结果：{}".format(parameter))

        # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
        expected_rs = case_data['check_body']['expected_result']
        __relevance = readRelevance.get_relevance(parameter, expected_rs, __relevance)
        expected_rs = replaceRelevance.replace(expected_rs, __relevance)
        case_data['check_body']['expected_result'] = expected_rs
        logging.debug("期望返回处理结果：{}".format(case_data))

    return test_info, case_data
