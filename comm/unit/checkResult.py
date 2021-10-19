# -*- coding:utf-8 -*-
# @Time    : 2021/2/2
# @Author  : Leo Zhang
# @File    : checkResult.py
# ***************************
import re
import allure
import operator
import logging
from decimal import Decimal


def check_json(src_data, dst_data):
    """
    校验的json
    :param src_data: 检验内容
    :param dst_data: 接口返回的数据
    :return:
    """
    if isinstance(src_data, dict):
        for key in src_data:
            if key not in dst_data:
                raise Exception("JSON格式校验，关键字 %s 不在返回结果 %s 中！" % (key, dst_data))
            else:
                this_key = key
                if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                    check_json(src_data[this_key], dst_data[this_key])
                elif not isinstance(src_data[this_key], type(dst_data[this_key])):
                    raise Exception("JSON格式校验，关键字 %s 返回结果 %s 与期望结果 %s 类型不符"
                                    % (this_key, src_data[this_key], dst_data[this_key]))
                else:
                    pass
    else:
        raise Exception("JSON校验内容非dict格式：{}".format(src_data))


def check_database(actual, expected, mark=''):
    """校验数据库

    :param actual: 实际结果
    :param expected: 期望结果
    :param mark: 标识
    :return:
    """
    if isinstance(actual, dict) and isinstance(expected, dict):
        result = list()
        logging.info('校验数据库{}>>>'.format(mark))
        content = '\n%(key)-20s%(actual)-40s%(expected)-40s%(result)-10s' \
                % {'key': 'KEY', 'actual': 'ACTUAL', 'expected': 'EXPECTED', 'result': 'RESULT'}
        for key in expected:
            if key in actual:
                actual_value = actual[key]
            else:
                actual_value = None
            expected_value = expected[key]
            if actual_value or expected_value:
                if isinstance(actual_value, (int, float, Decimal)):
                    if int(actual_value) == int(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
                else:
                    if str(actual_value) == str(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
            else:
                rst = 'PASS'
            result.append(rst)
            line = '%(key)-20s%(actual)-40s%(expected)-40s%(result)-10s' \
                % {'key': key, 'actual': str(actual_value) + ' ',
                            'expected': str(expected_value) + ' ', 'result': rst}
            content = content + '\n' + line
        logging.info(content)
        allure.attach(name="校验数据库详情{}".format(mark[-1]), body=str(content))
        if 'FAIL' in result:
            raise AssertionError('校验数据库{}未通过！'.format(mark))

    elif isinstance(actual, list) and isinstance(expected, list):
        result = list()
        logging.info('校验数据库{}>>>'.format(mark))
        content = '\n%(key)-25s%(actual)-35s%(expected)-35s%(result)-10s' \
                % {'key': 'INDEX', 'actual': 'ACTUAL', 'expected': 'EXPECTED', 'result': 'RESULT'}
        for index in range(len(expected)):
            if index < len(actual):
                actual_value = actual[index]
            else:
                actual_value = None
            expected_value = expected[index]
            if actual_value or expected_value:
                if isinstance(actual_value, (int, float, Decimal)):
                    if int(actual_value) == int(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
                else:
                    if str(actual_value) == str(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
            else:
                rst = 'PASS'
            result.append(rst)
            line = '%(key)-25s%(actual)-35s%(expected)-35s%(result)-10s' \
                % {'key': index, 'actual': str(actual_value) + ' ',
                            'expected': str(expected_value) + ' ', 'result': rst}
            content = content + '\n' + line
        logging.info(content)
        allure.attach(name="校验数据库详情{}".format(mark[-1]), body=str(content))
        if 'FAIL' in result:
            raise AssertionError('校验数据库{}未通过！'.format(mark))

    else:
        logging.info('校验数据库{}>>>'.format(mark))
        logging.info('ACTUAL: {}\nEXPECTED: {}'.format(actual, expected))
        if str(expected) != str(actual):
            raise AssertionError('校验数据库{}未通过！'.format(mark))


def check_result(case_data, code, data):
    """
    校验测试结果
    :param case_data: 用例数据
    :param code: 接口状态码
    :param data: 返回的接口json数据
    :return:
    """
    try:
        # 获取用例检查信息
        check_type = case_data['check_body']['check_type']
        expected_code = case_data['check_body']['expected_code']
        expected_result = case_data['check_body']['expected_result']
    except Exception as e:
        raise KeyError('获取用例检查信息失败：{}'.format(e))

    # 接口数据校验
    if check_type == 'no_check':
        with allure.step("不校验接口结果"):
            pass

    elif check_type == 'check_code':
        with allure.step("仅校验接口状态码"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
        if int(code) != int(expected_code):
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'check_contain':
        with allure.step("校验接口结果包含"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
            allure.attach(name='期望data', body=str(expected_result))
        if int(code) == int(expected_code):
            if not data:
                data = ""
            for each in expected_result:
                if str(each) not in str(data):
                    raise Exception("包含校验失败！ %s not in %s" % (expected_result, data))
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'check_json':
        with allure.step("JSON格式校验接口"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
            allure.attach(name='期望data', body=str(expected_result))
        if int(code) == int(expected_code):
            if not data:
                data = "{}"
            check_json(expected_result, data)
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'entirely_check':
        with allure.step("完全校验接口结果"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
            allure.attach(name='期望data', body=str(expected_result))
        if int(code) == int(expected_code):
            result = operator.eq(expected_result, data)
            if not result:
                raise Exception("完全校验失败！ %s ! = %s" % (expected_result, data))
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'regular_check':
        if int(code) == int(expected_code):
            try:
                result = ""
                if isinstance(expected_result, list):
                    for i in expected_result:
                        result = re.findall(i.replace("\"", "\""), str(data))
                        allure.attach('校验完成结果\n', str(result))
                else:
                    result = re.findall(expected_result.replace("\"", "\'"), str(data))
                    with allure.step("正则校验接口结果"):
                        allure.attach(name="实际code", body=str(code))
                        allure.attach(name="期望code", body=str(expected_code))
                        allure.attach(name='实际data', body=str(data))
                        allure.attach(name='期望data', body=str(expected_result).replace("\'", "\""))
                        allure.attach(name=expected_result.replace("\"", "\'") + '校验完成结果',
                                      body=str(result).replace("\'", "\""))
                if not result:
                    raise Exception("正则未校验到内容！ %s" % expected_result)
            except KeyError:
                raise Exception("正则校验执行失败！ %s\n正则表达式为空时" % expected_result)
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    else:
        raise Exception("无该接口校验方式%s" % check_type)