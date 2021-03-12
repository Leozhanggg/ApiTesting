# -*- coding:utf-8 -*-
# @Time    : 2020/12/10
# @Author  : Leo Zhang
# @File    : randomly.py
# *************************
import string
import random
import datetime
from dateutil.relativedelta import relativedelta


def random_str(str_len):
	"""从a-zA-Z0-9生成制定数量的随机字符

	:param str_len: 字符串长度
	:return:
	"""
	try:
		str_len = int(str_len)
	except ValueError:
		raise Exception("调用随机字符失败，[ %s ]长度参数有误！" % str_len)
	strings = ''.join(random.sample(string.hexdigits, +str_len))
	return strings


def random_int(scope):
	"""获取随机整型数据

	:param scope: 数据范围
	:return:
	"""
	try:
		start_num, end_num = scope.split(",")
		start_num = int(start_num)
		end_num = int(end_num)
	except ValueError:
		raise Exception("调用随机整数失败，[ %s ]范围参数有误！" % str(scope))
	if start_num <= end_num:
		number = random.randint(start_num, end_num)
	else:
		number = random.randint(end_num, start_num)
	return number


def random_float(data):
	"""获取随机浮点数据

	:param data: 数组
	:return:
	"""
	try:
		start_num, end_num, accuracy = data.split(",")
		start_num = int(start_num)
		end_num = int(end_num)
		accuracy = int(accuracy)
	except ValueError:
		raise Exception("调用随机浮点数失败，[ %s ]范围参数或精度有误！" % data)

	if start_num <= end_num:
		number = random.uniform(start_num, end_num)
	else:
		number = random.uniform(end_num, start_num)
	number = round(number, accuracy)
	return number


def random_choice(data):
	"""获取数组随机值

	:param data: 数组
	:return:
	"""
	_list = data.split(",")
	each = random.choice(_list)
	return each


def get_date_mark(now, mark, num):
	if 'y' == mark:
		return now + relativedelta(years=num)
	elif 'm' == mark:
		return now + relativedelta(months=num)
	elif 'd' == mark:
		return now + relativedelta(days=num)
	elif 'h' == mark:
		return now + relativedelta(hours=num)
	elif 'M' == mark:
		return now + relativedelta(minutes=num)
	elif 's' == mark:
		return now + relativedelta(seconds=num)
	else:
		raise Exception("日期字段标识[ %s ]错误, 请使用[年y,月m,日d,时h,分M,秒s]标识!" % mark)


def generate_date(expr=''):
	"""生成日期对象(不含时分秒)

	:param expr: 日期表达式，如"d-1"代表日期减1
	:return:
	"""
	today = datetime.date.today()
	if expr:
		try:
			mark = expr[:1]
			num = int(expr[1:])
		except (TypeError, NameError):
			raise Exception("调用生成日期失败，日期表达式[ %s ]有误！" % expr)
		return get_date_mark(today, mark, num)
	else:
		return today


def generate_datetime(expr=''):
	"""生成日期时间对象(含时分秒)

	:param expr: 日期表达式，如"d-1"代表日期减1
	:return:
	"""
	now = datetime.datetime.now().replace(microsecond=0)
	if expr:
		try:
			mark = expr[:1]
			num = int(expr[1:])
		except (TypeError, NameError):
			raise Exception("调用生成日期失败，日期表达式[ %s ]有误！" % expr)
		return get_date_mark(now, mark, num)
	else:
		return now


def generate_timestamp(expr=''):
	"""生成时间戳(13位)

	:param expr: 日期表达式，如"d-1"代表日期减1
	:return:
	"""
	datetime_obj = generate_datetime(expr)
	return int(datetime.datetime.timestamp(datetime_obj)) * 1000


def generate_guid():
	"""基于MAC地址+时间戳+随机数来生成GUID

	:param:
	:return:
	"""
	import uuid
	return str(uuid.uuid1()).upper()


def generate_wxid():
	"""基于AUTO标识+26位英文字母大小写+数字生成伪微信ID

	:param:
	:return:
	"""
	return 'AUTO' + ''.join(random.sample(string.ascii_letters + string.digits, 24))


def generate_noid(expr=''):
	"""基于6位随机数字+出生日期+4位随机数生成伪身份证

	:param expr: 日期表达式，如"d-1"代表日期减1
	:return:
	"""
	birthday = generate_date(expr)
	birthday = str(birthday).replace('-', '')
	return int(str(random.randint(100000, 999999)) + birthday + str(random.randint(1000, 9999)))


def generate_phone():
	"""基于三大运营商号段+随机数生成伪手机号

	:param:
	:return:
	"""
	ctcc = [133,153,173,177,180,181,189,191,193,199]
	cucc = [130,131,132,155,156,166,175,176,185,186,166]
	cmcc = [134,135,136,137,138,139,147,150,151,152,157,158,159,172,178,182,183,184,187,188,198]
	begin = 10 ** 7
	end = 10 ** 8 - 1
	prefix = random.choice(ctcc+cucc+cmcc)
	return str(prefix) + str(random.randint(begin, end))


if __name__ == '__main__':
	# 简单随机数据
	print(random_str(16))
	print(random_int("100,200"))
	print(random_float("200,100,5"))
	print(random_choice("aaa,bbb,ccc"))

	# 生成日期数据
	print(generate_date())
	print(generate_datetime())
	print(generate_date('m+1'))
	print(generate_datetime('d+1'))
	print(generate_timestamp('s+100'))
	print(generate_noid('y-18'))

	# 生成常用数据
	print(generate_guid())
	print(generate_wxid())
	print(generate_noid())
	print(generate_phone())