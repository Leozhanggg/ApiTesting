# -*- coding:utf-8 -*-
# @Time    : 2021/2/2
# @Author  : Leo Zhang
# @File    : test_initCanSelInfo.py
# ****************************
import os
import allure
import pytest
from comm.utils.readYaml import read_yaml_data
from comm.unit.initializePremise import init_premise
from comm.unit.apiSend import send_request
from comm.unit.checkResult import check_result
file_path = os.path.realpath(__file__).replace('\\', '/')
case_yaml = file_path.replace('/testcase/', '/page/').replace('.py', '.yaml')
test_case = read_yaml_data(case_yaml)


@allure.feature(test_case["test_info"]["title"])
class TestRegister:

    @pytest.mark.parametrize("test_case", test_case["test_case"])
    @allure.story("test_initCanSelInfo")
    def test_initCanSelInfo(self, test_case):
        # 初始化请求：执行前置接口+替换关联变量
        test_info, test_case = init_premise(test_case["test_info"], test_case, case_yaml)
        # 发送当前接口
        code, data = send_request(test_info, test_case)
        # 校验接口返回
        check_result(test_case, code, data)
