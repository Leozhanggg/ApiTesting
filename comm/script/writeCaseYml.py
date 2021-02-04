# -*- coding:utf-8 -*-
# @Time    : 2020/10/15
# @Author  : Leo Zhang
# @File    : writeCaseYaml.py
# ****************************
import os
import json
import logging
import urllib.parse
from comm.utils.readYaml import write_yaml_file, read_yaml_data
from comm.utils.readJson import write_json_file
from config import API_CONFIG, PROJECT_NAME


def write_case_yaml(har_path):
    """循环读取接口数据文件

    :param har_path: Charles导出文件路径
    :return:
    """
    case_file_list = list()
    logging.debug("读取文件主目录: {}".format(har_path))
    har_list = os.listdir(har_path)
    for each in har_list:
        ext_name = os.path.splitext(each)[1]
        if ext_name == '.chlsj':

            logging.debug("读取抓包文件: {}".format(each))
            file_path = har_path+'/'+each
            with open(file_path, 'r', encoding='utf-8') as f:
                har_cts = json.loads(f.read())
                har_ct = har_cts[0]

                # 获取接口基本信息
                host = har_ct["host"]
                port = har_ct["port"]
                method = har_ct["method"]
                path = har_ct["path"]
                headers = har_ct["request"]["header"]['headers']
                title = path.split("/")[-1]
                module = path.split("/")[-2]

                # 创建模块目录
                module_path = har_path.split('data')[0] + '/page/' + module
                try:
                    os.makedirs(module_path)
                except:
                    pass

                # 定义api通过配置
                api_config = dict()
                simp_header = dict()
                for each in headers:
                    # 去除基础请求头
                    base_header = ['Host',
                                   'Content-Length',
                                   'User-Agent',
                                   'Origin',
                                   'Referer',
                                   'Connection',
                                   'Accept',
                                   'Accept-Encoding',
                                   'Accept-Language']
                    if each['name'] not in base_header:
                        simp_header[each['name']] = each['value']
                api_config['host'] = host+':'+str(port)
                # 判断是否存在自定义消息头
                if simp_header:
                    api_config['headers'] = simp_header
                else:
                    api_config['headers'] = None
                api_config['cookies'] = None
                # 检查是否已存在项目配置信息，没有则写入
                rconfig = read_yaml_data(API_CONFIG)
                if rconfig:
                    if PROJECT_NAME not in rconfig:
                        rconfig[PROJECT_NAME] = api_config
                        write_yaml_file(API_CONFIG, rconfig)
                else:
                    nconfig = dict()
                    nconfig[PROJECT_NAME] = api_config
                    write_yaml_file(API_CONFIG, nconfig)

                # 定义测试信息
                test_info = dict()
                test_info["title"] = module
                test_info["host"] = '${host}'
                test_info["scheme"] = har_ct["scheme"]
                test_info["method"] = method
                test_info["address"] = path
                test_info["mime_type"] = har_ct["request"]["mimeType"]
                test_info["headers"] = '${headers}'
                test_info["timeout"] = 10
                test_info["file"] = False
                test_info["cookies"] = False
                test_info["premise"] = False

                # 解析请求报文
                parameter = dict()
                try:
                    if method in 'POST':
                        parameter_list = urllib.parse.unquote(har_ct["request"]["body"]["text"])
                    elif method in 'PUT':
                        parameter_list = har_ct["request"]["body"]["text"]
                    elif method in 'DELETE':
                        parameter_list = urllib.parse.unquote(har_ct["request"]["body"]["text"])
                    else:
                        parameter_list = har_ct["query"]

                    if "&" in parameter_list:
                        for key in parameter_list.split("&"):
                            val = key.split("=")
                            parameter[val[0]] = val[1]
                    else:
                        parameter = json.loads(parameter_list)
                except Exception as e:
                    logging.error("未找到parameter: %s" % e)
                    raise e

                # 定义用例信息
                test_case_list = list()
                test_case = dict()
                test_case["summary"] = title
                test_case["describe"] = 'test_'+title

                # 定义请求入参信息，且当参数字符总长度大于200时单独写入json文件
                if len(str(parameter)) > 200:
                    param_name = title+'_request.json'
                    if param_name not in os.listdir(module_path):
                        # 定义请求json
                        param_dict = dict()
                        param_dict["summary"] = title
                        param_dict["body"] = parameter
                        param_file = module_path+'/'+param_name
                        write_json_file(param_file, [param_dict])
                    test_case["parameter"] = param_name
                else:
                    test_case["parameter"] = parameter

                # 定义请求返回信息
                response_code = har_ct["response"]["status"]
                response_body = har_ct["response"]["body"]["text"]
                check = dict()
                check["check_type"] = 'check_json'
                check["expected_code"] = response_code
                expected_request = json.loads(response_body)

                # 当返回参数字符总长度大于200时单独写入json文件
                if len(str(expected_request)) > 200:
                    result_name = title+'_response.json'
                    if result_name not in os.listdir(module_path):
                        # 定义响应json
                        result_dict = dict()
                        result_dict["summary"] = title
                        result_dict["body"] = expected_request
                        result_file = module_path + '/' + result_name
                        write_json_file(result_file, [result_dict])
                    check["expected_result"] = result_name
                else:
                    check["expected_result"] = expected_request
                test_case["check"] = check
                test_case_list.append(test_case)

                # 合并测试信息、用例信息
                case_list = dict()
                case_list["test_info"] = test_info
                case_list["test_case"] = test_case_list

                # 写入测试用例(存在则忽略)
                case_name = 'test_'+title+'.yaml'
                case_file = module_path+'/'+case_name
                if not os.path.exists(case_file):
                    logging.debug("写入测试文件: {}".format(case_file))
                    write_yaml_file(case_file, case_list)

                case_file_list.append(case_file)
    return case_file_list


if __name__ == '__main__':
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    print('测试用例列表: ', write_case_yaml(real_path+'/data'))
