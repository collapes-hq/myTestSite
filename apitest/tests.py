from django.test import TestCase

# Create your tests here.

import subprocess


import json

a = {'123': '123', '234': '5234'}
print(type(a))
for k,v in a.items():
    print(k,v)
# #
# # print(json.loads(a))
#