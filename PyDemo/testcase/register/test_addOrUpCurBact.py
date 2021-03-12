# -*- coding:utf-8 -*-
# @Time    : 2021/2/2
# @Author  : Leo Zhang
# @File    : test_addOrUpCurBact.py
# ****************************
import os
import allure
import pytest
from comm.utils.readYaml import read_yaml_data
from comm.unit.initializePremise import init_premise
from comm.unit.apiSend import send_request
from comm.unit.checkResult import check_result
case_yaml = os.path.realpath(__file__).replace('testcase', 'page').replace('.py', '.yaml')
case_path = os.path.dirname(case_yaml)
case_dict = read_yaml_data(case_yaml)


@allure.feature(case_dict["test_info"]["title"])
class TestRegister:

    @pytest.mark.parametrize("case_data", case_dict["test_case"])
    @allure.story("test_addOrUpCurBact")
    def test_addOrUpCurBact(self, case_data):
        # 初始化请求：执行前置接口+替换关联变量
        test_info, case_data = init_premise(case_dict["test_info"], case_data, case_path)
        # 发送当前接口
        code, data = send_request(test_info, case_data)
        # 校验接口返回
        check_result(case_data, code, data)
