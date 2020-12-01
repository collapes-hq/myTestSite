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


