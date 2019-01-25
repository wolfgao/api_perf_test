# -*- coding: utf-8 -*-

'''
	This file is tring to run locust without web interface, please refer to 
	https://docs.locust.io/en/stable/running-locust-without-web-ui.html
	Why do we need to do that? Generally because we have to integrate this job to our CI, when the build is out,
	CI will trigger that to perform the tests automatically.
'''
import os
import subprocess
from lib import utils

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RESULTS_PATH = os.path.join(PATH + "/outputs/")
REPORTS_PATH = os.path.join(PATH + "/reports/")

print("The current path is %s" %PATH)
print("The result path is %s" %RESULTS_PATH)
print("The report path is %s" %REPORTS_PATH)

#获得配置字典表
d = utils.get_values_from_yaml(PATH+'/locust_conf.yml')

if __name__ == '__main__':

	current_num = d['current_num']	
	hatch_rate = d['hatch-rate']
	url = d['servers'][0]['host']

	# $ locust -f locust_files/my_locust_file.py --no-web -c 1000 -r 100
	#If you want to specify the run time for a test, you can do that with --run-time or -t:
	locust_command = "locust -f locust_test.py --host=%s --no-web -c %d -r %d" %(url, current_num, hatch_rate)
	print(locust_command)
	(status, result) = subprocess.getstatusoutput(locust_command)
	print(status)
	print(result)
