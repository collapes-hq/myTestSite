from django.test import TestCase

# Create your tests here.

import subprocess

import json

# a = {'123': '123', '234': '5234'}
# print(type(a))
# for k,v in a.items():
#     print(k,v)
# # #
# # # print(json.loads(a))
# #

# a = "/api/addcase/6/"
# print(a.split('/'))

# target = 'hiouahiou'
# for i in target:
#     if target.count(i) == 1:
#         print(target.index(i))
#         break

# a= 'they are boy'
# b=list(a)
# print(b)
# c = 'aeiou'
# for i in c:
#     if i in b:
#         b.pop()
# a = '12345'
# for i in range(0, len(a)-1):
#     print(i)
# a = (('技术部', (367, 500, 45)), ('人力资源部', (247, 368, 1280)), ('财务部', (87, 100, 24, 50)))
#
# sumcount = 0
# for i in a:
#     for j in i[1]:
#         sumcount +=j
# print(sumcount)
#
# sumcount = 10000
# name = ''
# for i in a:
#     s_sumcount = 0
#     for j in i[1]:
#         s_sumcount += j
#     if sumcount > s_sumcount:
#         sumcount = s_sumcount
#         name = i[0]
# print(name)
# print(sumcount)

#
# a = ((5, 7), (18, 20), (19, 37), (56, 58))
# b = (6, 19, 47, 57, 86)
# in_count = 0
# for i in b:
#     for j in a:
#         if i >= j[0] and i <= j[1]:
#             in_count += 1
# print(in_count)

# a = 'title=华为春季新品发布会&sign=323dwd&limit=100&status=0&address=国家会议中心&time=2018-03-28'
# b = []
# for i in a.split('&'):
#     if i.startswith('sign'):
#         i = 'sign=1234'
#     b.append(i)
# print('&'.join(b))


# import os
#
# f = os.popen('ifconfig')
# shuchu = f.read()
# result = shuchu.split("\n")
# new_result = [item.strip() for item in result]
# print(new_result)


# import subprocess
#
# result = subprocess.run('ifconfig', stdout=subprocess.PIPE)
# print(type(result))
# print(result.returncode)
# a = result.stdout.decode('utf-8')
# print(type(a))
# # result = subprocess.check_output('ifconfig')
# # # print(type(result.stdout)) # <class 'bytes'>
# # # print(result.stdout.decode('utf-8'))
# # print(result)
#
# # result = subprocess.getoutput('ifconfig')
# # print(result)
# # result1 = subprocess.getstatusoutput('ifconfig')
# # print(result1[1])
#
#
# # result = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, universal_newlines=True)
# # result1 = subprocess.Popen('ifconfig', stdout=subprocess.PIPE, encoding='utf-8')
# # result2 = subprocess.run('ifconfig', stdout=subprocess.PIPE)
# # print(result1)
# # print(type(result2.stdout.decode('utf-8')))
# a = '[1,2,3,4,5]'
# n=a.split(',')
# print(n)
# print(list(n)[3])
# import grequests
#
# a = 'http://httpbin.org/get?a=1&b=2'
#
#
# def print_url(r, *args, **kwargs):
#     print(1111)
#     print(r.url)


# url = "http://www.baidu.com"
# req_list = []
# req_list.append(grequests.get('http://121.36.69.137/getmockjson', headers={"a": "b"}))
# # response = grequests.get('http://121.36.69.137/getmockjson')
#
# resp = grequests.map(req_list)
# print(resp[0].request.headers)
# print(resp[0].text)
# import requests
# try:
#     resp = requests.get('http://121.36.69.137/getmockjson', headers={"a": "b"})
#     print(resp.status_code, resp.request.headers)
# except Exception as e:
#     print(e)
#
#
# print(resp.text)
# print(type(resp.text))
# import time
# print(time.localtime())
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
# time.sleep(10)
# print(time.localtime())

# from apitest import tasks
#
# res = tasks.addaaa.delay()
#
# print(res.get())