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
from config import PAGE_DIR, PROJECT_NAME, API_CONFIG
from comm.unit import apiSend, readRelevance, replaceRelevance
from comm.utils import readYaml


def read_json(summary, json_obj, case_path):
    """
    校验内容读取
    :param summary: 用例名称
    :param json_obj: json文件或数据对象
    :param case_path: case路径
    :return:
    """
    if not json_obj or isinstance(json_obj, dict):
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


def pre_send_request(pre_case_yaml, relevance):
    """
    调用前置接口并返回响应消息体
    :param pre_case_yaml: 前置用例相对路径
    :param relevance: 关联值对象
    :return:
    """
    # 获取前置接口用例
    logging.info("获取前置接口测试用例：{}".format(pre_case_yaml))
    pre_case_yaml = PAGE_DIR + pre_case_yaml
    pre_case_path = os.path.dirname(pre_case_yaml)
    pre_case_data = readYaml.read_yaml_data(pre_case_yaml)
    pre_test_info = pre_case_data['test_info']
    pre_test_case = pre_case_data['test_case'][0]

    # 判断前置接口是否也存在前置接口
    if pre_test_info["premise"]:
        init_premise(pre_test_info, pre_test_case, pre_case_yaml)

    for i in range(3):
        # 处理前置接口测试信息
        pre_test_info = replaceRelevance.replace(pre_test_info, relevance)
        logging.debug("测试信息处理结果：{}".format(pre_test_info))

        # 处理前置接口入参：获取入参-替换关联值-发送请求
        pre_parameter = read_json(pre_test_case['summary'], pre_test_case['parameter'], pre_case_path)
        pre_parameter = replaceRelevance.replace(pre_parameter, relevance)
        pre_test_case['parameter'] = pre_parameter
        logging.debug("请求参数处理结果：{}".format(pre_parameter))
        logging.info("执行前置接口测试用例：{}".format(pre_test_info))
        code, data = apiSend.send_request(pre_test_info, pre_test_case)
        # 检查接口是否调用成功
        if data:
            return data
        else:
            time.sleep(1)
            logging.error("前置接口请求失败！等待1秒后重试！")
    else:
        logging.info("前置接口请求失败！尝试三次失败！")
        raise Exception("获取前置接口关联数据失败！")


def init_premise(test_info, test_case, case_yaml):
    """用例前提条件执行，提取关键值

    :param test_info: 测试信息
    :param test_case: 测试数据
    :param case_yaml: 用例路径
    :return:
    """
    case_path = os.path.dirname(case_yaml)
    # 获取项目公共关联值
    aconfig = readYaml.read_yaml_data(API_CONFIG)
    __relevance = aconfig[PROJECT_NAME]
    # 处理测试信息
    test_info = replaceRelevance.replace(test_info, __relevance)
    logging.debug("测试信息处理结果：{}".format(test_info))

    # 判断是否存在前置接口
    pre_case_yaml = test_info["premise"]
    if pre_case_yaml:
        if isinstance(pre_case_yaml, list):
            data = []
            for each in pre_case_yaml:
                each_data = pre_send_request(each, __relevance.copy())
                data.append(each_data)
        else:
            data = pre_send_request(pre_case_yaml, __relevance.copy())

        # 处理当前接口入参：获取入参-获取关联值-替换关联值
        parameter = read_json(test_case['summary'], test_case['parameter'], case_path)
        __relevance = readRelevance.get_relevance(data, parameter, __relevance)
        parameter = replaceRelevance.replace(parameter, __relevance)
        test_case['parameter'] = parameter
        logging.debug("请求参数处理结果：{}".format(parameter))

        # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
        expected_rs = read_json(test_case['summary'], test_case['check_body']['expected_result'], case_path)
        # msg_body = parameter.copy()
        # msg_body['pre_response'] = data
        # __relevance = readRelevance.get_relevance(msg_body, expected_rs, __relevance)
        __relevance = readRelevance.get_relevance(data, expected_rs, __relevance)
        expected_rs = replaceRelevance.replace(expected_rs, __relevance)
        test_case['check_body']['expected_result'] = expected_rs
        logging.debug("期望返回处理结果：{}".format(test_case))

    else:
        # 处理当前接口入参：获取入参-获取关联值-替换关联值
        parameter = read_json(test_case['summary'], test_case['parameter'], case_path)
        parameter = replaceRelevance.replace(parameter, __relevance)
        test_case['parameter'] = parameter
        logging.debug("请求参数处理结果：{}".format(parameter))

        # 获取当前接口期望结果：获取期望结果-获取关联值-替换关联值
        expected_rs = read_json(test_case['summary'], test_case['check_body']['expected_result'], case_path)
        # __relevance = readRelevance.get_relevance(parameter, expected_rs, __relevance)
        expected_rs = replaceRelevance.replace(expected_rs, __relevance)
        test_case['check_body']['expected_result'] = expected_rs
        logging.debug("期望返回处理结果：{}".format(test_case))

    return test_info, test_case
