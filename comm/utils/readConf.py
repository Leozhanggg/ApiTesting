# -*- coding:utf-8 -*-
# @Time    : 2020/12/03
# @Author  : Leo Zhang
# @File    : readConf.py
# ***********************
import codecs
import configparser


class ReadConf:

    def __init__(self, cfg_path):
        """
        配置文件初始化
        :param cfg_path:
        """
        fd = open(cfg_path.replace('\\', '/'), encoding='utf-8')
        data = fd.read()
        # 去除配置文件开头编码标识
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            files = codecs.open(cfg_path, "w")
            files.write(data)
            files.close()
        fd.close()
        self.cf = configparser.ConfigParser()
        self.cf.read(cfg_path, encoding='utf-8-sig')

    def get_sections(self):
        """
        获取所有条目
        :return:
        """
        return self.cf.sections()

    def get_items(self, section):
        """
        获取指定条目下所有键值对
        :param section:
        :return:
        """
        return self.cf.items(section)

    def get_options(self, section):
        """
        获取指定条目下所有键值
        :param section:
        :return:
        """
        return self.cf.options(section)

    def get_value(self, section, option):
        """
        获取指定条目指定键的值
        :param section:
        :param option:
        :return:
        """
        return self.cf.get(section, option)

    def has_section(self, section):
        """
        返回是否存在指定条目
        :param section:
        :return:
        """
        return self.cf.has_section(section)

    def has_option(self, section, option):
        """
        返回指定条目是否存在指定键
        :param section:
        :param option:
        :return:
        """
        return self.cf.has_option(section, option)
