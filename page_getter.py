# -*- coding: utf-8 -*-
import requests
from lxml import html
import sys
import json
import time
import re
from progress_bar import progress

'''Parsing page with ad to get user information'''

with open('state_name.txt', 'r', encoding = 'utf-8') as f:
	state_name = f.read()

if len(sys.argv) == 4:

	def get_html(url):
		if url.find('https://dom.ria.com')!=-1:
			return r.get(url, headers=hdrs).text
		else:
			raise Exception("Invalid input")

	STATE_FILE = sys.argv[1]
	N = int(sys.argv[2])
	THREADS_NUM = int(sys.argv[3])

	base_url = "https://dom.ria.com/node/api/getOwnerAndAgencyDataByIds?userId={}&agencyId={}&langId={}&_csrf={}"
	dom_ria_url = "https://dom.ria.com/ru/"
	hdrs = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, br',
			'Referer': 'https://dom.ria.com/ru/search/',
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
			}
			
	pages = []

	with open(STATE_FILE, 'r') as f:
		urls = list(json.load(f).values())

	for i in range(0, len(urls), THREADS_NUM):
		progress(i, len(urls), status = "Getting pages info")
		tries=0
		if i+N < len(urls):
			while(True):
				try:
					r = requests.Session()
					url = urls[i+N]

					page = {
						'name':'',
						'type':'',
						'agency':'',
						'term':'',
						'offers':'',
						'state':'',
						'city':'',
						'phones':[]
					}

					html_code = html.fromstring(get_html(dom_ria_url + url))

					csrf = html_code.xpath('//script[contains(@src,"require.js")]/@data-csrf')[0]
					lang_id = html_code.xpath('//script[contains(@src,"require.js")]/@data-lang-id')[0]
					owner_div_content = html_code.xpath('//div[contains(@class,"heading-dom")]/script//text()')[0]
					user_id = re.search('\"user_id\":([0-9]+),', owner_div_content).group(1)
					agency_id = re.search('\"agency_id\":([0-9]+),', owner_div_content)
					if agency_id!=None:
						agency_id = agency_id.group(1)
					else:
						agency_id = 0

					script_tag = html.fromstring(html_code.xpath('//script[contains(@id, "finalPageUserInfoBlockPhonesTemplate")]//text()')[0])
					category_id = script_tag.xpath('//a/@realty_category_id')[0]

					content = r.get(base_url.format(user_id, agency_id, lang_id, csrf))

					user_info = json.loads(content.text)

					hdrs_details = {
						'Accept-Encoding':'gzip, deflate, br',
						'Referer': url,
						'Accept': 'application/json, text/javascript, */*; q=0.01',
						'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
						'Content-Length': '26',
						'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
						'Origin': 'https://dom.ria.com',
						'x-requested-with': 'XMLHttpRequest',
						'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
						}

					realties = json.loads(r.post("https://dom.ria.com/node/api/getRealtiesCount", data = 'user_id={}&category={}'.format(user_id, category_id), headers = hdrs_details).text)
					
					if user_info['owner'].get('state_name','')==state_name:

						page['name'] = user_info['owner']['name']
						page['offers'] = realties['allCount']
						page['type'] = 'продавец' if agency_id==0 else 'риелтор'
						page['agency'] = user_info['agency']['agency_name'] if agency_id!=0 else ''
						page['term'] = user_info['owner']['uses_site']
						page['state'] = user_info['owner'].get('state_name','')
						page['city'] = user_info['owner'].get('city_name','')
						for phone in user_info['owner']['owner_phones']:
							page['phones'].append(phone["phone_formatted"])
						page['phones'] = list(map(lambda x: "38"+x.replace(')','').replace('(','').replace(' ','').replace('-',''), page['phones']))

						pages.append(page)

					break
				except Exception as e:
					if tries==3:

						break
					tries+=1



	with open('user{}.json'.format(N),'w') as f:
		json.dump(pages, f)
	progress(100, 100, status = "Getting pages info")
