# -*- coding: utf-8 -*-

import os,sys
from time import sleep
import yaml
import unittest
import subprocess

from locust import Locust, TaskSet, task
from locust import HttpLocust
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
# Returns abs path relative to this file and not cwd
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RESULTS_PATH = os.path.join(PATH + "/outputs/")
REPORTS_PATH = os.path.join(PATH + "/reports/")

print("The current path is %s" %PATH)
print("The result path is %s" %RESULTS_PATH)
print("The report path is %s" %REPORTS_PATH)

class UserBehavior(TaskSet):
    #下面应该是压测时候的比重
    tasks = {index: 2, profile: 1}

    @task
    def login(self):
		'''
			Post example
		'''
		#根据你网站的实际情况填写
	    self.head = {'Content-Type': 'application/json; charset=utf-8',
	    				'token': 'xxxx',
	    				'User-Agent': 'xxx',
	    				'userId': 'xxxx'
	    			}
	   	self.form_data = {'account': 'admin',
	   						'password': 'adminxxx'}
	   	r = self.client.post('/path/login', headers=self.head, data = json.dumps(self.form_data)) 
	    result = r.json()
	    assert r.json['code'] == 200
	    print(result)

	@task
	def logout(self):
		'''
			同上,一样处理
		'''
	    self.client.post("/logout", {"account":"admin", "password":"xxx"})
	    result = r.json()
	    assert r.json['code'] == 200

	@task
	def index(self):
		'''
			get example
		'''
	    self.client.get("/")
	    result = r.json()
	    assert r.json['code'] == 200

	@task
	def profile(self):	
	    self.client.get("/profile")
	    result = r.json()
	    assert r.json['code'] == 200
    
   
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

if __name__ == '__main__':
	#print(d['perform_num'])

	(status, result) = subprocess.getstatusoutput(ab_command)
