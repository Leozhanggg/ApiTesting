# -*- coding:utf-8 -*-
# @Time    : 2021/2/2
# @Author  : Leo Zhang
# @File    : test_case.py
# ****************************
import os
import allure
import pytest
from comm.unit.initializePremise import init_premise
from comm.unit.apiSend import send_request
from comm.unit.checkResult import check_result
from comm.utils.readYaml import read_yaml_data, write_yaml_file
from comm.script import init_case
excel = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_case.xlsx')
test_data_1, test_name_1 = init_case.get_test_data(excel, '普通租户开立')
# test_data_2, test_name_2 = init_case.get_test_data(excel, 'Sheet2')


@allure.feature('测试框架')
class TestFramework:

    def save_token(self, case_data, rsp_data):
        config = str(os.path.realpath(__file__)).split('testcase')[0] + 'config.yml'
        if case_data['test_info']['address'] == '/api/blade-auth/oauth/token':
            # 把获取的token保存配置文件中
            cfg = read_yaml_data(config)
            cfg['headers']['Blade-Auth'] = 'Bearer ' + rsp_data['access_token']
            write_yaml_file(config, cfg)

    @allure.story('测试集1')
    @pytest.mark.parametrize("case_data", test_data_1, ids=test_name_1)
    def test_sheet1(self, case_data):
        # 初始化请求：执行前置接口+替换关联变量
        test_info, test_case = init_premise(case_data['test_info'], case_data['test_case'], test_data_1)
        # 发送当前接口
        code, data = send_request(test_info, test_case)
        # 校验接口返回
        check_result(test_case, code, data)
        # 保存token
        self.save_token(case_data, data)

    # @allure.story('测试集2')
    # @pytest.mark.parametrize("case_data", test_data_2, ids=test_name_2)
    # def test_demo(self, case_data):
    #     # 初始化请求：执行前置接口+替换关联变量
    #     test_info, test_case = init_premise(case_data['test_info'], case_data['test_case'], test_data_2)
    #     # 发送当前接口
    #     code, data = send_request(test_info, test_case)
    #     # 校验接口返回
    #     check_result(test_case, code, data)
    #     # 保存token
    #     self.save_token(case_data)
