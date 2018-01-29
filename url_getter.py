import requests
import json
from progress_bar import progress

STATE_ID = 0
with open('state_id.txt', 'r') as f:
	STATE_ID = int(f.readline())
try:
	with open('users/users{}.json'.format(STATE_ID), 'r') as f:
		users = json.load(f)
except Exception as e:
	users = []

try:
	with open('states/state{}.json'.format(STATE_ID), 'r') as f:
		items_list = json.load(f)
		items = dict.fromkeys(items_list, '')
except Exception as e:
	items = []
	print('Error reading file')

if len(items) > 0:
	counter = 0
	total = len(items_list)
	r = requests.Session()
	headers = {'accept':'application/json, text/javascript, */*; q=0.01','accept-encoding':'gzip, deflate, br','accept-language':'ru,uk;q=0.9,en;q=0.8,de;q=0.7','referer':'https://dom.ria.com/ru/search/?','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36','x-requested-with':'XMLHttpRequest'}
	for item_id in items_list:
		progress(counter, total-1, status = "Getting urls")
		tries = 0
		while True:
			if tries == 3:
				try:
					del items[item_id]
					counter+=1
					break
				except Exception as e:
					counter+=1
					break
			tries += 1
			try:
				resp = json.loads(r.get('https://dom.ria.com/node/searchEngine/v2/view/realty/{}'.format(item_id), headers=headers).text)
				user_id = resp['user_id']
				url = resp['beautiful_url']
				if user_id in users:
					del items[item_id]
					counter+=1
					break
				else:
					items[item_id] = url
					users.append(user_id)
					counter+=1
					break
			except Exception as e:
				counter+=1
				continue

	with open('users/users{}.json'.format(STATE_ID), 'w') as f:
		json.dump(users, f)

	with open('states/state{}.json'.format(STATE_ID), 'w') as f:
		json.dump(items, f)