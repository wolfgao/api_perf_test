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
    两种执行方式：
    1） 一种是web形式，更直观，可以随时调整参数和获得结果，图形化展现结果非常好使；
    2）另一种是命令行方式，必须带有 -f 文件，就是locust_xxx.py这种配置文件
    否则报错：
    locust -H http://www.baidu.com
    [2019-01-24 13:32:31,933] GaochuangMac.local/ERROR/locust.main: Could not find any locustfile! Ensure file ends in '.py'
    下面捡重要的options说一下：
    -h, --help            show this help message and exit
    -H HOST, --host=HOST  Host to load test in the following format:
                        http://10.21.32.33
    --web-host=WEB_HOST   Host to bind the web interface to. Defaults to '' (all interfaces)
    -P PORT, --port=PORT, --web-port=PORT Port on which to run web host
    -f LOCUSTFILE, --locustfile=LOCUSTFILE python module file to import, e.g. '../other.py'.
                        Default: locustfile
    --csv=CSVFILEBASE, --csv-base-name=CSVFILEBASE
                        Store current request stats to files in CSV format.
    --master              Set locust to run in distributed mode with this process as master
    --slave               Set locust to run in distributed mode with this process as slave
    ...
    -c NUM_CLIENTS, --clients=NUM_CLIENTS
                        Number of concurrent Locust users. Only used together with --no-web
    -r HATCH_RATE, --hatch-rate=HATCH_RATE
                        The rate per second in which clients are spawned. Only used together with --no-web
    -t RUN_TIME, --run-time=RUN_TIME
                        Stop after the specified amount of time, e.g. (300s, 20m, 3h, 1h30m, etc.). Only used together with --no-
                        web
    -L LOGLEVEL, --loglevel=LOGLEVEL
                        Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL. Default is INFO.
    --logfile=LOGFILE     Path to log file. If not set, log will go to
                        stdout/stderr
    --print-stats         Print stats in the console
    --only-summary        Only print the summary stats
    ...
'''
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RESULTS_PATH = os.path.join(PATH + "/outputs/")
REPORTS_PATH = os.path.join(PATH + "/reports/")

print("The current path is %s" %PATH)
print("The result path is %s" %RESULTS_PATH)
print("The report path is %s" %REPORTS_PATH)

#获得配置字典表
d = utils.get_values_from_yaml(PATH+'/locust_conf.yml')

login_url = d['login_url']
account = d['account']
password = d['password']

class UserBehavior(TaskSet):
  @task(1)
  def login(self):
    #Post example - 根据你网站的实际情况填写
    self.head = {'Content-Type':'application/json; charset=utf-8',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    self.form_data = {'account':account, 'password':password}
    self.client.headers.update(self.head)
    #print(self.client.headers)

    response = self.client.post(login_url, data=self.form_data)
    print("The result of \'login post\' test is : %s" %response)
    assert(response.status_code ==200)

  '''
  这部分也是需要根据实际情况来编写，可以效仿login的案例  
  @task(1)
  def logout(self):
  #同上,一样处理
    self.client.post("/logout", {"account":"admin", "password":"xxx"})
    result = r.json()
    assert r.json['code'] == 200
  '''  
  #@task takes an optional weight argument that can be used to specify the task’s execution ratio. 
  #In the following example task2 will be executed twice as much as task1:
  
  @task(2)
  def index(self):
    response = self.client.get("/")
    print("The result of \'get test\' is %s." %response)
    assert(response.status_code ==200)  
  '''
  @task(1)
  def profile(self):	
    self.client.get("/profile")
    result = r.json()
    assert r.json['code'] == 200
  '''
class WebsiteUser(HttpLocust):
  '''
    websiteuser类:用于设置性能测试
    task_set ：定义一个用户行为类
    min_wait ：执行事务之间用户等待时间的下界（ms）
    max_wait: 用户等待时间的上界
  '''
  task_set = UserBehavior
  min_wait = 5000
  max_wait = 9000


