# -*- coding:utf-8 -*-
# @Time    : 2020/12/03
# @Author  : Leo Zhang
# @File    : readJson.py
# ***********************
import json


def read_json_data(json_file):
	"""读取json文件数据

	:param json_file: json文件地址
	:return:
	"""
	with open(json_file, "r", encoding="utf-8") as fr:
		return json.load(fr)


def write_json_file(json_file, obj):
	"""把对象obj写入json文件

	:param json_file: json文件地址
	:param obj: 数据对象
	:return:
	"""
	with open(json_file, "w", encoding='utf-8') as fw:
		json.dump(obj, fw, ensure_ascii=False, indent=4)
