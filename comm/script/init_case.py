# -*- coding:utf-8 -*-
# @Time    : 2021/10/17
# @Author  : Leo Zhang
# @File    : init_case.py
# ****************************
import json
import xlrd
import logging


def get_test_data(excel, sheet):
    test_data = list()
    test_name = list()
    logging.info("正在获取excel：{}".format(excel))
    wb = xlrd.open_workbook(excel)
    sheet_names = wb.sheet_names()

    # 循环获取每一个sheet
    for each in sheet_names:
        if each != sheet:
            continue
        logging.info("正在获取sheet：{}".format(each))
        sheet_data = wb.sheet_by_name(each)
        nrows = sheet_data.nrows
        ncols = sheet_data.ncols

        # 判断是否执行该sheet
        is_run = sheet_data.cell_value(0, 0)
        if nrows < 2 or is_run != 'is_skip':
            logging.info("无效sheet，跳过!")
            continue

        # 循环获取每一行
        for row in range(1, nrows):
            # 定义测试数据格式
            case = {
                'test_info': {
                    'host': '${host}',
                    'scheme': '${scheme}',
                    'timeout': 10,
                    'file': '',
                    'cookies': ''
                },
                'test_case': {
                    'check_body': {}
                }
            }
            test_case_keys = ['summary', 'describe', 'parameter']
            check_body_keys = ['check_type', 'expected_code', 'expected_result']
            json_keys = ['headers', 'parameter', 'expected_result']

            # 循环获取每一列
            for col in range(ncols):
                key = sheet_data.cell_value(0, col)
                value = sheet_data.cell_value(row, col)
                if isinstance(value, str):
                    value = value.replace('\n', '').strip(' ')
                if key in json_keys and value and value != '${headers}':
                    try:
                        value = json.loads(value)
                    except json.decoder.JSONDecodeError as e:
                        logging.exception(e)
                        logging.error("json格式错误：{}".format(value))

                # 判断用例信息
                if key in test_case_keys:
                    case['test_case'][key] = value
                elif key in check_body_keys:
                    case['test_case']['check_body'][key] = value
                else:
                    case['test_info'][key] = value

            if case['test_info']['is_skip']:
                continue
            else:
                test_data.append(case)
                test_name.append(case['test_case']['summary'])
                logging.info("正在获取用例：{}".format(case))
        logging.info("获取测试数据完成!")
        return test_data, test_name
