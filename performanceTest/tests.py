# Create your tests here.

import subprocess

import os
# s = os.getcwd()
# print(s)

import time

# cur_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
# result_jtl = os.path.join('/tmp/result', '{0}.jtl'.format(cur_time))
# print(result_jtl)
#
# jmx_dir_path = os.path.join(os.path.dirname(__file__), 'jmeterFiles/jmxFiles')
# demo_jmx = os.path.join(jmx_dir_path, 'demo.jmx')
# print(demo_jmx)
# # 根据task_id新建
# new_task_jmx = os.path.join(jmx_dir_path, '{0}-{1}.jmx'.format('123', str(cur_time)))
#
# task_jmx = 'test.jmx'
# remote_ip = '10.0.0.1'
# command = "jmeter -n -t {task_jmx} -R {remote_ip} -l {result_jtl} -e -o /temp/result/{cur_time}-report".format(
#     task_jmx=new_task_jmx, remote_ip=remote_ip, result_jtl=result_jtl, cur_time=cur_time)
#
# print(command)
import time
from subprocess import Popen, PIPE, STDOUT
#
# print("start-time is :" + str(time.time()))
# command = "/home/jmeter/apache-jmeter-5.3/bin/jmeter -n -t /home/jmeter/scripts/testnginx.jmx -R 150.158.157.58 -l /home/jmeter/scripts/test2.jtl -e -o /home/jmeter/scripts/report2"
# # command ="df -h"
# p = Popen("jmeter -n -t /home/hq/gitproject/myTestSite/performanceTest/jmeterFiles/jmxFiles/28-2020-11-24-16_26_55.jmx -R 150.158.157.58 -l /tmp/result/2020-11-24-16-26-55.jtl -e -o /tmp/result/2020-11-24-16-26-55-report", shell=True, stdout=subprocess.PIPE,env=None, stderr=subprocess.STDOUT)
# out = p.stdout.readlines()
# print(out)
# print("end-time is :" + str(time.time()))
import json
file = '/tmp/result/2020-11-24-13_12_59-report/statistics.json'
with open(file,'r') as f:

    result = json.load(f)

print(type(result))
print(result)
print(result['Total'])
print(result['Total']['sampleCount'])