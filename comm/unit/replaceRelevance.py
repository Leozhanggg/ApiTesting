# -*- coding:utf-8 -*-
# @Time    : 2020/12/09
# @Author  : Leo Zhang
# @File    : replaceRelevance.py
# ****************************
import re
from comm.utils.randomly import *

pattern_var = r"\${(.*?)}"
pattern_eval = r"\$Eval\((.*?)\)"
pattern_str = r'\$RandStr\(([0-9]*?)\)'
pattern_int = r'\$RandInt\(([0-9]*,[0-9]*?)\)'
pattern_choice = r"\$RandChoice\((.*?)\)"
pattern_float = r'\$RandFloat\(([0-9]*,[0-9]*,[0-9]*)\)'
pattern_phone = r'\$GenPhone\(\)'
pattern_guid = r'\$GenGuid\(\)'
pattern_wxid = r'\$GenWxid\(\)'
pattern_noid = r'\$GenNoid\((.*?)\)'
pattern_date = r'\$GenDate\((.*?)\)'
pattern_datetime = r'\$GenDatetime\((.*?)\)'


def replace_pattern(pattern, value):
	"""替换正则表达式

	:param pattern: 匹配字符
	:param value: 匹配值
	:return:
	"""
	patterns = pattern.split('(.*?)')
	return ''.join([patterns[0], value, patterns[-1]])


def replace_relevance(param, relevance=None):
	"""替换变量关联值

	:param param: 参数对象
	:param relevance: 关联对象
	:return:
	"""
	result = re.findall(pattern_var, str(param))
	if (not result) or (not relevance):
		pass
	else:
		for each in result:
			try:
				# 关联值只考虑一个值
				# value = relevance[each]
				# pattern = re.compile(r'\${' + each + '}')
				# try:
				# 	param = re.sub(pattern, value, param)
				# except TypeError:
				# 	param = value

				# 关联参数多值时一一对应替换
				# relevance_index = 0
				# if isinstance(relevance[each], list):
				# 	try:
				# 		param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
				# 		relevance_index += 1
				# 	except IndexError:
				# 		relevance_index = 0
				# 		param = re.sub(pattern, relevance[each][relevance_index], param, count=1)
				# 		relevance_index += 1

				# 关联参数多值时指定索引值替换
				mark = re.findall(r"\[\-?[0-9]*\]", each)
				# 判断关联参数是否指定索引值var[n]
				if len(mark)==0:
					if isinstance(relevance[each], list):
						value = relevance[each][0]
					else:
						value = relevance[each]
				elif len(mark)==1:
					var = each.strip(mark[0])
					n = int(mark[0].strip('[').strip(']'))
					value = relevance[var][n]
					each = each.replace('[', '\[').replace(']', '\]')
				else:
					var = each
					for m in mark:
						var = var.replace(m, '')
					n1 = int(mark[0].strip('[').strip(']'))
					n2 = int(mark[1].strip('[').strip(']'))
					value = relevance[var][n1][n2]
					each = each.replace('[', '\[').replace(']', '\]')

				# 生成正在表达式并替换关联参数
				pattern = re.compile('\${' + each + '}')
				try:
					if param.strip('${' + each + '}'):
						param = re.sub(pattern, str(value), param)
					else:
						param = re.sub(pattern, value, param)
				except TypeError:
					param = value
			except KeyError:
				raise KeyError('替换变量{0}失败，未发现变量对应关联值！\n关联列表：{1}'.format(param, relevance))
				# pass
	return param


def replace_eval(param):
	"""替换eval表达式结果

	:param param: 参数对象
	:return:
	"""
	result = re.findall(pattern_eval, str(param))
	if not result:
		pass
	else:
		for each in result:
			try:
				if 'import' in each:
					raise Exception('存在非法标识import')
				else:
					value = str(eval(each))
					param = re.sub(pattern_eval, value, param)
			except KeyError as e:
				raise Exception('获取值[ % ]失败！\n%'.format(param, e))
			except SyntaxError:
				pass
	return param


def replace_random(param):
	"""替换随机方法参数值

	:param param:
	:return:
	"""
	int_list = re.findall(pattern_int, str(param))
	str_list = re.findall(pattern_str, str(param))
	choice_list = re.findall(pattern_choice, str(param))
	guid_list = re.findall(pattern_guid, str(param))
	noid_list = re.findall(pattern_noid, str(param))
	phone_list = re.findall(pattern_phone, str(param))
	wxid_list = re.findall(pattern_wxid, str(param))
	date_list = re.findall(pattern_date, str(param))
	datetime_list = re.findall(pattern_datetime, str(param))

	if len(str_list):
		for each in str_list:
			# pattern = re.compile(r'\$RandStr\(' + each + r'\)')
			# param = re.sub(pattern, str(random_str(each)), param, count=1)
			param = re.sub(pattern_str, str(random_str(each)), param, count=1)

	if len(int_list):
		for each in int_list:
			param = re.sub(pattern_int, str(random_int(each)), param, count=1)

	if len(choice_list):
		for each in choice_list:
			param = re.sub(pattern_choice, str(random_choice(each)), param, count=1)

	if len(date_list):
		for each in date_list:
			param = re.sub(pattern_date, str(generate_date(each)), param, count=1)

	if len(datetime_list):
		for each in datetime_list:
			param = re.sub(pattern_datetime, str(generate_datetime(each)), param, count=1)

	if len(noid_list):
		for each in noid_list:
			param = re.sub(pattern_noid, str(generate_noid(each)), param, count=1)

	if len(phone_list):
		for i in phone_list:
			param = re.sub(pattern_phone, str(generate_phone()), param, count=1)

	if len(guid_list):
		for i in guid_list:
			param = re.sub(pattern_guid, generate_guid(), param, count=1)

	if len(wxid_list):
		for i in wxid_list:
			param = re.sub(pattern_wxid, generate_wxid(), param, count=1)

	return param


def replace(param, relevance=None):
	"""替换参数对应关联数据

	:param param: 参数对象
	:param relevance: 关联对象
	:return:
	"""
	if not param:
		pass
	elif isinstance(param, dict):
		for key, value in param.items():
			if isinstance(value, dict):
				param[key] = replace(value, relevance)
			elif isinstance(value, list):
				for index, sub_value in enumerate(value):
					param[key][index] = replace(sub_value, relevance)
			else:
				value = replace_relevance(value, relevance)
				value = replace_random(value)
				value = replace_eval(value)
				param[key] = value

	elif isinstance(param, list):
		for index, value in enumerate(param):
			param[index] = replace(value, relevance)

	else:
		param = replace_relevance(param, relevance)
		param = replace_random(param)
		param = replace_eval(param)

	return param


if __name__ == '__main__':
	print('替换变量并计算表达式：', replace('$Eval(${unitCode}*1000+1)', {'unitCode': 9876543210}))
	print('生成1-9之间的随机数：', replace('$RandInt(1,9)'))
	print('生成10位随机字符：', replace('$RandStr(10)'))
	print('从列表中随机选择：', replace('$RandChoice(a,b,c,d)'))
	print('生成一个伪手机号：', replace('$GenPhone()'))
	print('生成一个guid：', replace('$GenGuid()'))
	print('生成一个伪微信ID：', replace('$GenWxid()'))
	print('生成一个伪身份证：', replace('$GenNoid()'))
	print('生成一个18岁伪身份证：', replace("$GenNoid(y-18)"))
	print('生成下个月今天的日期：', replace("$GenDate(m+1)"))
	print('生成昨天此时的时间：', replace("$GenDatetime(d-1)"))
	print('通过索引指定关联值：', replace('${name[-1]}', {'name': ['test1', 'test2']}))
