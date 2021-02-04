# -*- coding:utf-8 -*-
# @Time    : 2020/12/03
# @Author  : Leo Zhang
# @File    : readYaml.py
# ***********************


def read_yaml_data(yaml_file):
	"""读取yaml文件数据

	:param yaml_file: yaml文件地址
	:return:
	"""
	import yaml
	with open(yaml_file, 'r', encoding="utf-8") as fr:
		return yaml.load(fr, Loader=yaml.SafeLoader)


def write_yaml_file(yaml_file, obj):
	"""把对象obj写入yaml文件

	:param yaml_file: yaml文件地址
	:param obj: 数据对象
	:return:
	"""
	from ruamel import yaml
	with open(yaml_file, 'w', encoding='utf-8') as fw:
		yaml.dump(obj, fw, Dumper=yaml.RoundTripDumper, allow_unicode=True)
