# -*- coding:utf-8 -*-
# @Time    : 2021/2/2
# @Author  : Leo Zhang
# @File    : apiMethod.py
# *************************
import os
import json
import random
import logging
import requests
import simplejson
from requests_toolbelt import MultipartEncoder
from comm.utils.readYaml import write_yaml_file, read_yaml_data
from config import API_CONFIG, PROJECT_NAME


def post(headers, address, mime_type, timeout=10, data=None, files=None, cookies=None):
    """
    post请求
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 上传文件请求参数（dict）
    :param cookies:
    :return:
    """
    # 判断请求参数类型
    if 'form_data' in mime_type:
        for key in files:
            value = files[key]
            # 判定参数值是否为文件，如果是则替换为二进制值
            if '/' in value:
                files[key] = (os.path.basename(value), open(value, 'rb'))
        enc = MultipartEncoder(
            fields=files,
            boundary='--------------' + str(random.randint(1e28, 1e29-1))
        )
        headers['Content-Type'] = enc.content_type
        response = requests.post(url=address,
                                 data=enc,
                                 headers=headers,
                                 timeout=timeout,
                                 cookies=cookies,
                                 verify=False)
    elif 'application/json' in mime_type:
        response = requests.post(url=address,
                                 data=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies,
                                 verify=False)
    else:
        response = requests.post(url=address,
                                 json=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies,
                                 verify=False)
    try:
        if response.status_code != 200:
            return response.status_code, response.text
        else:
            return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def get(headers, address, data, timeout=8, cookies=None):
    """
    get请求
    :param headers: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :param cookies:
    :return:
    """
    response = requests.get(url=address,
                            params=data,
                            headers=headers,
                            timeout=timeout,
                            cookies=cookies,
                            verify=False)
    if response.status_code == 301:
        response = requests.get(url=response.headers["location"], verify=False)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def put(headers, address, mime_type, timeout=8, data=None, files=None, cookies=None):
    """
    put请求
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :param cookies:
    :return:
    """
    if mime_type == 'raw':
        data = json.dumps(data)
    elif mime_type == 'application/json':
        data = json.dumps(data)
    response = requests.put(url=address,
                            data=data,
                            headers=headers,
                            timeout=timeout,
                            files=files,
                            cookies=cookies,
                            verify=False)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def delete(headers, address, data, timeout=8, cookies=None):
    """
    delete请求
    :param headers: 请求头
    :param address: 请求地址
    :param data: 请求参数
    :param timeout: 超时时间
    :param cookies:
    :return:
    """
    response = requests.delete(url=address,
                               params=data,
                               headers=headers,
                               timeout=timeout,
                               cookies=cookies,
                               verify=False)
    try:
        return response.status_code, response.json()
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise


def save_cookie(headers, address, mime_type, timeout=8, data=None, files=None, cookies=None):
    """
    保存cookie信息
    :param headers: 请求头
    :param address: 请求地址
    :param mime_type: 请求参数格式（form_data,raw）
    :param timeout: 超时时间
    :param data: 请求参数
    :param files: 文件路径
    :param cookies:
    :return:
    """
    if 'data' in mime_type:
        response = requests.post(url=address,
                                 data=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies,
                                 verify=False)
    else:
        response = requests.post(url=address,
                                 json=data,
                                 headers=headers,
                                 timeout=timeout,
                                 files=files,
                                 cookies=cookies,
                                 verify=False)
    try:
        cookies = response.cookies.get_dict()
        # 读取api配置并写入最新的cookie结果
        aconfig = read_yaml_data(API_CONFIG)
        aconfig[PROJECT_NAME]['cookies'] = cookies
        write_yaml_file(API_CONFIG, aconfig)
        logging.debug("cookies已保存，结果为：{}".format(cookies))
    except json.decoder.JSONDecodeError:
        return response.status_code, None
    except simplejson.errors.JSONDecodeError:
        return response.status_code, None
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        raise
