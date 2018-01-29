# -*- coding: utf-8 -*-
import json
import multiprocessing
import os
import requests
import time
import sys
from xls_builder import build_xls
from subprocess import Popen
import os


t = time.time()

THREADS_NUM = 10
threads = []
SYS_EXECUTABLE = sys.executable
if not os.path.exists('users'):
	os.mkdir('users')
if not os.path.exists('states'):
	os.mkdir('states')
if not os.path.exists('xls'):
	os.mkdir('xls')
STATE_ID = 0
try:
	with open('state_id.txt', 'r') as f:
		STATE_ID = int(f.readline())
except Exception as e:
	print("No file state_id.txt")
	while(STATE_ID < 1 or STATE_ID > 25):
		STATE_ID = input("Enter id from 1 to 25.\n")
		try:
			STATE_ID = int(STATE_ID)
		except Exception:
			STATE_ID = 0

with open('state_id.txt', 'w') as f:
	f.write(str(STATE_ID))
	

state_name = requests.get('https://dom.ria.com/node/api/getStates?lang_id=2')
for i in json.loads(state_name.text):
	if i['stateID']==STATE_ID:
		with open('state_name.txt','w', encoding = 'utf-8') as f:
			f.write(i['name'])

state_file = "states/state{}.json".format(STATE_ID)

adv_thread = Popen([SYS_EXECUTABLE, os.path.dirname(os.path.abspath(__file__)) + '/adverts_getter.py'])
adv_thread.wait()
print()

url_thread = Popen([SYS_EXECUTABLE, os.path.dirname(os.path.abspath(__file__)) + '/url_getter.py'])
url_thread.wait()
print()

for i in range(THREADS_NUM):
	threads.append(Popen([SYS_EXECUTABLE, os.path.dirname(os.path.abspath(__file__)) + '/page_getter.py', state_file, str(i), str(THREADS_NUM)]))

for thread in threads:
	thread.wait()

print()

if os.path.exists('users/state{}.json'.format(STATE_ID)):
	with open('users/state{}.json'.format(STATE_ID),'r') as f:
		user_info = json.load(f)
else:
	user_info = []
for i in range(THREADS_NUM):
	with open('user{}.json'.format(i), 'r') as f:
		user_info.extend(json.load(f))
	os.remove('user{}.json'.format(i))
with open('users/state{}.json'.format(STATE_ID),'w') as f:
	json.dump(user_info, f)

if os.path.exists('xls/state{}.xls'.format(STATE_ID)):
	os.remove('xls/state{}.xls'.format(STATE_ID))
build_xls('users/state{}.json'.format(STATE_ID), "xls/state{}.xls".format(STATE_ID))
print("\nBuilding took {}s".format(round(time.time()-t, 2)))