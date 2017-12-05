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