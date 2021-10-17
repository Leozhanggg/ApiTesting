# -*- coding:utf-8 -*-
# @Time    : 2021/10/17
# @Author  : Leo Zhang
# @File    : startup.py
# ***********************
import os
import pytest

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.realpath(__file__))
    log_dir = root_dir+'/logs'
    report_xml = root_dir+'/report/xml'
    report_html = root_dir+'/report/html'

    from comm.utils import writeLogs
    writeLogs.MyLogs(log_dir)

    pytest.main(['-vs', 'testcase', '--alluredir', report_xml, '--clean-alluredir', '--disable-warnings'])

    # 生成allure报告
    cmd = 'allure generate --clean %s -o %s ' % (report_xml, report_html)
    os.system(cmd)