# -*- coding: utf-8 -*-

import os,sys
from time import sleep
import unittest
import subprocess
from lib import utils

'''
ab命令格式如下： 
ab [options] [http[s]://]hostname[:port]/path
这个“/”非常重要，如果你输入ab http://www.baidu.com会提示你invalid url，但是加上“/”后就okay。
Options are:
    -n requests     Number of requests to perform，请求个数
    -c concurrency  Number of multiple requests to make at a time，1个请求的并发访问数
    -t timelimit    Seconds to max. to spend on benchmarking
                    This implies -n 50000
    -s timeout      Seconds to max. wait for each response
                    Default is 30 seconds
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -B address      Address to bind to when making outgoing connections
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header to use for POST/PUT data, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -q              Do not show progress when doing more than 150 requests
    -l              Accept variable document length (use this for dynamic pages)
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -m method       Method name
    -h              Display usage information (this message)
    -I              Disable TLS Server Name Indication (SNI) extension
    -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
    -f protocol     Specify SSL/TLS protocol
                    (TLS1, TLS1.1, TLS1.2 or ALL)
需要注意的是：ab每次只能测试一个URL，适合做重复压力测试，支持POST方式。
'''

# Returns abs path relative to this file and not cwd
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RESULTS_PATH = os.path.join(PATH + "/outputs/")
REPORTS_PATH = os.path.join(PATH + "/reports/")

print("The current path is %s" %PATH)
print("The result path is %s" %RESULTS_PATH)
print("The report path is %s" %REPORTS_PATH)

d = utils.get_values_from_yaml(PATH+'/ab_conf.yml')

def ab_format():
	'''
		从配置文件读取每一个case的配置，然后组合成ab命令
		返回一个list
	'''
	cases = d['perform_num']
	ab_commands = []
	if len(cases) >1:
		i=0
		for case in cases:
			ab_command = d['ab_path']
			case = d['perform_num'][i]
			case_id = case['case']
			current_num = case['current_num']
			request_max = case['request_max']
			url = case['url']
			ab_command += " -n %s -c %s %s" %(request_max ,current_num ,url)
			print("Case #%s command is %s" %(case_id, ab_command))
			i+=1
			ab_commands.append(ab_command)

			#ab_command += "ab %s %s" % %url
	else:
		pass
	return ab_commands

def htmlreport(result):
	'''
		ToDo: 需要完成，根据需求将测试结果加工成html report
		https://pypi.org/project/HTMLReport/
		HTMLReport是一个单元测试测试运行器，可以将测试结果保存在 Html 文件中，用于人性化的结果显示。
		仅支持Python 3.x
		因此如果要使用需要安装： pip3 install HTMLReport
		import unittest
		import HTMLReport
	'''
	pass

def handle_result(result):
	'''
		根据result形成想要的报告:1）将详细结果存档；2）将报告整理加工形成报告，或者集成到测试平台
	'''
	detail_result_file = os.path.join(RESULTS_PATH+"results.txt")
	f=open(detail_result_file, 'a+', encoding='utf-8')
	f.write(result+'\n')
	f.write('\n')
	f.write('--------------------------------- end of the case ------------------------------- ' +'\n')
	f.write('\n')
	f.close()
	htmlreport(result)


def run_test():
	ab_commands = ab_format()
	if ab_commands is not None:
		for ab_command in ab_commands:
			(status, result) = subprocess.getstatusoutput(ab_command)
			if status == 0: #成功执行
				handle_result(result)



if __name__ == '__main__':
	#print(d['perform_num'])
	run_test()