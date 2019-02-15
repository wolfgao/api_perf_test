# -*- coding: utf-8 -*-

import os,sys,subprocess
from time import sleep
import yaml
import unittest
import json

from locust import Locust, TaskSet, task
from locust import HttpLocust
from lib import utils
'''
此文件主要是为了配合CI，通过no-web的方式来执行，当然这里面需要一个终止信号。
我们可以通过它判断Totol等于某个数来完成。
'''

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RESULTS_PATH = os.path.join(PATH + "/outputs/")
REPORTS_PATH = os.path.join(PATH + "/reports/")

print("The current path is %s" %PATH)
print("The result path is %s" %RESULTS_PATH)
print("The report path is %s" %REPORTS_PATH)

#获得配置字典表
d = utils.get_values_from_yaml(PATH+'/locust_conf.yml')

if __name__ == '__main__':

  #获得运行参数
  current_num = d['current_num']  
  hatch_rate = d['hatch-rate']
  host = d['host']
  port = int(d['port'])
  
  # $ locust -f locust_files/my_locust_file.py --no-web -c 1000 -r 100
  #If you want to specify the run time for a test, you can do that with --run-time or -t:
  locust_command = "locust -f locust_login_demo.py --host=%s -P %d --no-web -c %d -r %d" %(host, port, current_num, hatch_rate)
  print(locust_command)
  #(status, result) = subprocess.getstatusoutput(locust_command)
  os.system(locust_command)
  print(status)
  print(result)
