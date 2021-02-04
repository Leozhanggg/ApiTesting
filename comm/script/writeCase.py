# -*- coding:utf-8 -*-
# @Time    : 2020/10/15
# @Author  : Leo Zhang
# @File    : writeCase.py
# ************************
import os
from config import ROOT_DIR
from comm.script.writeCaseYml import write_case_yaml, read_yaml_data
temp_file = ROOT_DIR+'config/test_template.py'


def write_case(case_path, auto_yaml=True):
    """

    :param case_path: 用例路径，当auto_yaml为True时，需要传入data目录，否则传入扫描目录
    :param auto_yaml: 是否自动生成yaml文件
    :return:
    """
    # 判断是否自动生成yaml用例
    if auto_yaml:
        yaml_list = write_case_yaml(case_path)
    else:
        yaml_list = list()
        file_list = os.listdir(case_path)
        for file in file_list:
            if '.yaml' in file:
                yaml_path = case_path+'/'+file
                yaml_list.append(yaml_path)

    # 遍历测试用例列表
    for yaml_file in yaml_list:
        test_data = read_yaml_data(yaml_file)
        test_script = yaml_file.replace('page', 'testcase').replace('yaml', 'py')
        # case_name = os.path.basename(test_script).replace('.py', '')
        case_path = os.path.dirname(test_script)
        # 判断文件路径是否存在
        if not os.path.exists(case_path):
            os.makedirs(case_path)

        # 替换模板内容
        file_data = ''
        with open(temp_file, "r", encoding="utf-8") as f:
            for line in f:
                if 'TestTemplate' in line:
                    title = test_data['test_info']['title']
                    line = line.replace('Template', title.title())
                if 'test_template' in line:
                    if '@allure.story' in line:
                        describe = test_data['test_case'][0]['describe']
                        line = line.replace('test_template', describe)
                    else:
                        summary = test_data['test_case'][0]['summary']
                        line = line.replace('template', summary)
                file_data += line

        # 写入新脚本
        with open(test_script, "w", encoding="utf-8") as f:
            f.write(file_data)


if __name__ == '__main__':
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    write_case(real_path + '/data', auto_yaml=True)
    # write_case(real_path+'/page/oauth', auto_yaml=False)
