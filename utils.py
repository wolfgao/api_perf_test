
# -*- coding: utf-8 -*-
import os, sys
import yaml

'''
	一个工具类获取yml文件和其内容
'''

def get_values_from_yaml(yaml_file):
    f = open(yaml_file, 'r', encoding='utf-8')
    cfg = f.read()
    #print(type(cfg))  # 读出来是字符串
    #print(cfg)

    #获取字典表
    d = yaml.load(cfg)  # 用load方法转字典
    return d
