import paramiko
import time
import shutil
import logging
import logging.config
import re
import os

result = '''
7
Key             	Value
---             	-----
refresh_interval	768h0m0s
descritpion     	root
password        	xvc76DMiJpFXuF2TBemS

[e214375@rundeckppr1 ~]$'''

print(''.join(re.findall(r'password\s+(.*?)\s+', result)))

result = "root@10.114.27.106's password:"

print(result.endswith('password:'))

result = 'javascript:openEncodedURL("https://10.180.19.18/maximo/ui/1512455563060?_tbldnld=results_showlist&uisessionid=55&csrftoken=6dbm30ic01hkidbqmijaeb4gh7")'

print(''.join(re.findall(r'"(.*)"',result)))


str = '''avbd
'''+result+'''
345'''
print(str)

str='sr5537'
print(str.upper())

str='5625'
print('SR'+''.join(re.findall('\d+',str)))