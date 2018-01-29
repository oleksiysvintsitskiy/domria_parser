import requests
import json
from progress_bar import progress

'''Simulating going through all pages in search engine of dom.ria to get urls'''

STATE_ID = 0
with open('state_id.txt', 'r') as f:
	STATE_ID = int(f.readline())

try:
	with open('states/state{}.json'.format(STATE_ID), 'r') as f:
		items = set(json.load(f))
except Exception as e:
	items = set()

page = 1
page_items = 100
last_page = float("inf")
while page <= last_page:
	progress(page, last_page, status = "Collecting state pages")
	r = requests.get('https://dom.ria.com/node/searchEngine/v2/?page={}&limit={}&from_realty_id=&to_realty_id=&sort=inspected_sort&user_id=&category=&realty_type=&operation_type=&state_id={}&city_id%5B0%5D=&realty_id_only=&date_from=&date_to=&with_phone=&exclude_my=&new_housing_only=&banks_only='.format(page, page_items, STATE_ID), headers={'accept':'application/json, text/javascript, */*; q=0.01','accept-encoding':'gzip, deflate, br','accept-language':'ru,uk;q=0.9,en;q=0.8,de;q=0.7','referer':'https://dom.ria.com/ru/search/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36','x-requested-with':'XMLHttpRequest'})
	obj = json.loads(r.text)

	last_page = int(obj['count'] / page_items)
	for item in obj['items']:
		items.add(item)

	page += 1

with open('states/state{}.json'.format(STATE_ID), 'w') as f:
	json.dump(list(items), f)
