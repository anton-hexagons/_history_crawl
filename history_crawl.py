import os
import sys
import math
import json
import urllib.request
from html.parser import HTMLParser


wiki_history_url = '/wiki/History'
max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0
max_depth_reached = False

img_min_res = 100

page_url_list = []
img_page_url_list = []
img_other_black_list = []
url_black_list = ['#', '/wiki/Wikipedia:Protection_policy#semi', '#mw-head', '#p-search', '/wiki/List_of_national_legal_systems']
url_type_black_list = ['license']


in_content = False
page_thumbinner = False
page_thumbcaption = False
page_thumbcaption_magnify = False
img_page_urls = []
img_caption = ''
img_captions = []
# img_other_urls = []
page_sub_url_packs = []
# heading_title = ''
# hit_heading = False

class HTMLParser__wiki_page(HTMLParser):

	def handle_starttag(self, tag, attrs):

		global in_content
		global page_thumbinner
		global page_thumbcaption
		global page_thumbcaption_magnify
		global img_page_urls
		# global img_other_urls
		global page_sub_url_packs
		global hit_heading

		## page imgs from thumbinners
		if tag == 'div':
			for attr in attrs:
				if attr[0] == 'id':
					if attr[1] == 'content':
						in_content = True
						return
					if attr[1] == 'mw-navigation':
						in_content = False
						return
				if attr[0] == 'class':
					if attr[1] == 'thumbinner':
						page_thumbinner = True
						return
					if attr[1] == 'thumbcaption':
						page_thumbcaption = True
						return
					if page_thumbcaption:
						if attr[1] == 'magnify':
							page_thumbcaption_magnify = True
							return
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					if page_thumbinner:
						img_page_urls.append('https://en.wikipedia.org' + attr[1])
						return

		# if tag == 'h1':
		# 	for attr in attrs:
		# 		if attr[0] == 'id':
		# 			if attr[1] == 'firstHeading':
		# 				hit_heading = True
		
		if tag == 'img':
			if page_thumbinner:
				page_thumbinner = False
		# 	else:
		# 		page_img = {
		# 			'url': None,
		# 			'width': None,
		# 			'height': None
		# 		}
		# 		for attr in attrs:
		# 			if attr[0] == 'src':
		# 				page_img['url'] = 'https://' + attr[1][2:]
		# 			elif attr[0] == 'width':
		# 				page_img['width'] = int(attr[1])
		# 			elif attr[0] == 'height':
		# 				page_img['height'] = int(attr[1])
		# 		# if page_img['url']:
		# 		if page_img['width'] > img_min_res and page_img['height'] > img_min_res:
		# 			if page_img['url'] not in img_other_black_list:
		# 				img_other_urls.append(page_img['url'])

		lang_target = False
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'class':
					if attr[1] == 'interlanguage-link-target':
						lang_target = True

		if in_content or lang_target:
			## page url
			if tag == 'a':
				page_url_pack = {
					'title': '',
					'url': None
				}
				url_type = None
				for attr in attrs:
					if attr[0] == 'title':
						page_url_pack['title'] = attr[1]
					elif attr[0] == 'href':
						page_url_pack['url'] = attr[1]
					elif attr[0] == 'rel':
						url_type = attr[1]
				if page_url_pack['url']:
					if page_url_pack['url'] not in url_black_list:
						if url_type not in url_type_black_list:
							if page_url_pack['url'] not in page_url_list:
								page_sub_url_packs.append(page_url_pack)
								return

	def handle_data(self, data):

		global page_thumbcaption
		global img_caption

		if page_thumbcaption:
			img_caption += data

		# global hit_heading
		# global heading_title
		# if hit_heading:
		# 	heading_title = data
		# 	hit_heading = False

	def handle_endtag(self, tag):

		global page_thumbcaption_magnify
		global page_thumbcaption
		global img_caption
		global img_captions

		if tag == 'div':
			if page_thumbcaption_magnify:
				page_thumbcaption_magnify = False
			elif page_thumbcaption:
				img_captions.append(img_caption)
				img_caption = ''
				page_thumbcaption = False


def saveImg(img_url, img_file, wiki_img_folder):

	if img_url in img_page_url_list:
		print('img already saved globally:', img_url)
		return
	if len(img_file) > 100:
		img_file_name = '.'.join(img_file.split('.')[:-1])
		img_file_ext = img_file.split('.')[-1]
		img_file = img_file_name[:100] + '__.' + img_file_ext
		print('img file name too long, cropped at char 100, new file name:', img_file)
	if not os.path.exists(wiki_img_folder):
		os.makedirs(wiki_img_folder)
	img_file_path = os.path.join(wiki_img_folder, img_file)
	img_page_data['path'] = img_file_path
	if os.path.exists(img_file_path):
		print('img already saved, url:', img_url)
		return
	url = 'https://' + img_page_data['url']
	a = None
	try:
		a = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		print('img http error:', e.code, 'url:', url)
	except urllib.error.URLError as e:
		print('img url error, url:', url)
	if a:
		img_data = a.read()
		img_file = open(img_file_path, 'wb')
		img_file.write(img_data)
		img_page_url_list.append(img_url)
		print('img saved, url:', img_url)
	else:
		return


hit_org_img = False
# hit_description = False
hit_info_title = False
info_title = ''
hit_info_data = False
img_page_data = None
wiki_folder = ''

class HTMLParser__wiki_img_page(HTMLParser):

	def handle_starttag(self, tag, attrs):

		global hit_org_img
		# global hit_description
		global hit_info_title
		global img_page_data

		## org img
		if tag == 'div':
			for attr in attrs:
				if attr[0] == 'class':
					if attr[1] == 'fullMedia':
						hit_org_img = True
						return
					# if attr[1].startswith('description'):
					# 	hit_description = True

		## fileinfo
		if tag == 'td':
			for attr in attrs:
				if attr[0] == 'class':
					if attr[1] == 'fileinfo-paramfield':
						hit_info_title = True
						return
				
		if hit_org_img and tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					img_page_data['url'] = attr[1][2:]
			hit_org_img = False
			img_file = img_page_data['url'].split('/')[-1].replace('File:', '')
			saveImg('https://' + img_page_data['url'], img_file, os.path.join(wiki_folder, 'imgs'))
			img_file_path = os.path.join(wiki_folder, 'imgs', img_file)
			img_page_data['path'] = img_file_path
			return
		
		if tag == 'time':
			date = {
				'type': None,
				'date': None
			}
			for attr in attrs:
				if attr[0] == 'class':
					date['type'] = attr[1]
				if attr[0] == 'datetime':
					date['date'] = attr[1]
			img_page_data['date'] = date
			return

	def handle_data(self, data):

		# global hit_description
		global hit_info_title
		global info_title
		global hit_info_data
		global img_page_data

		# if hit_description:
		# 	img_page_data['description'] += data
		if hit_info_title:
			img_page_data['info'][data] = ''
			hit_info_title = None
			info_title = data
			hit_info_data = True
		elif hit_info_data:
			img_page_data['info'][info_title] += data

	def handle_endtag(self, tag):

		# global hit_description
		global hit_info_title
		global hit_info_data

		# if tag == 'div':
		# 	if hit_description:
		# 		hit_description = False
		if tag == 'td':	
			if hit_info_title == None:
				hit_info_title = False
			elif hit_info_data:
				hit_info_data = False
				info_title = ''


def Crawl__wiki_img_page(url):

	global img_page_data

	img_page_data = {
		'url': None,
		'date': None,
		# 'description': '',
		'info': {}
	}

	a = None
	try:
		a = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		print('img http error:', e.code, 'url:', url)
	except urllib.error.URLError as e:
		print('img url error, url:', url)
	if a:
		wiki_img_page = str(a.read())[2:-1]
		parser = HTMLParser__wiki_img_page()
		parser.feed(wiki_img_page)

def Crawl__wiki_page(url_pack, wiki_sub_folder):

	global max_depth
	global max_depth_reached
	global img_page_urls
	global img_captions
	global img_other_urls
	global page_sub_url_packs
	global img_page_data
	global heading_title
	global wiki_folder

	sub_wiki_depth = math.ceil((wiki_sub_folder.count(os.sep)) / 2)
	if sub_wiki_depth > max_depth:
		if not max_depth_reached:
			print('> max depth reached.')
			max_depth_reached = True
		return
	elif max_depth_reached:
		max_depth_reached = False

	if url_pack['url'] in page_url_list:
		print('> url already visited:', url_pack['url'])
		return
	else:
		print('> ' + ']' * sub_wiki_depth + ' wiki page')
		print('url_pack:', url_pack)
		print('wiki_sub_folder:', wiki_sub_folder)

	if url_pack['url'] in url_black_list:
		print('url in black list:', url_pack['url'])
		return

	if 'File:' in url_pack['url']:
		print('url is file:', url_pack['url'])
		return

	if url_pack['url'].startswith('#'):
		print('# url ignored:', url_pack['url'])
		return

	if url_pack['title'].startswith('wikt'):
		print('wikt url ignored:', url_pack['url'])
		return

	if url_pack['url'].startswith('//'):
		print('// url ignored:', url_pack['url'])
		return

	if 'http' in url_pack['url']:
		print('non wiki sub url, url ignored:', url_pack['url'])
		return

	if 'page_does_not_exist' in wiki_sub_folder:
		print('page_does_not_exist, sub folder:', wiki_sub_folder)
		return

	if 'disambiguation' in url_pack['title']:
		print('disambiguation in title, url:', url_pack['url'])
		return

	if 'ftp' in url_pack['url']:
		print('ftp url:', url_pack['url'])
		return

	# if '\\\\' in url_pack['title']:
	# 	print('decode:', url_pack['title'], '<<<<<<<<<<')
	# 	exit()
	# 	#codecs.decode(title.replace('\\x', ''), 'hex').decode(encoding='UTF-8',errors='strict')

	if '/' in url_pack['title']:
		url_pack['title'] = url_pack['title'].replace('/', '__')

	
	wiki_page_data = {
		'title': url_pack['title'],
		'url': 'https://en.wikipedia.org' + url_pack['url'],
		'img_packs': [],
		# 'imgs': [],
		'sub_url_packs': []
	}

	if wiki_page_data['title'] == None:
		wiki_page_data['title'] = ''

	## path
	json_file_name = 'wiki__' + wiki_page_data['title'].replace(' ', '_') + '.json'
	pyFileFolder = os.path.dirname(os.path.realpath(__file__))
	folder = os.path.join(pyFileFolder, 'wiki__History', wiki_sub_folder).replace(':', '__')
	if not os.path.exists(folder):
		os.makedirs(folder)
	wiki_folder = folder
	json_file_path = os.path.join(folder, json_file_name)


	if not os.path.exists(json_file_path):

		## wiki url parse
		a = None
		try:
			a = urllib.request.urlopen(wiki_page_data['url'])
		except urllib.error.HTTPError as e:
			print('http error:', e.code, 'url:', wiki_page_data['url'])
		except urllib.error.URLError as e:
			print('url error, url:', wiki_page_data['url'])
		if a:

			wiki_page = str(a.read())[2:-1]
			wiki_page_parser = HTMLParser__wiki_page()
			wiki_page_parser.feed(wiki_page)
			wiki_page_data['sub_url_packs'] = page_sub_url_packs
			page_sub_url_packs = []
		
			## wiki imgs parse
			for i in range(len(img_page_urls)):
				Crawl__wiki_img_page(img_page_urls[i])
				img_page_data['page_url'] = img_page_urls[i]
				if len(img_page_urls) == len(img_captions):
					img_page_data['img_caption'] = img_captions[i]
				wiki_page_data['img_packs'].append(img_page_data)
			img_page_urls = []
			img_captions = []

			## save json
			with open(json_file_path, 'w') as outfile:
				print(json.dumps(wiki_page_data, sort_keys=False, indent=4), file=outfile)
			
			## save html
			html_file_name = 'wiki__' + wiki_page_data['title'].replace(' ', '_') + '.html'
			html_file_path = os.path.join(folder, html_file_name)
			with open(html_file_path, 'w') as outfile:
				print(wiki_page, file=outfile)

			# ## wiki other imgs
			# for img_other_url in img_other_urls:
			# 	img_file = img_other_url.split('/')[-1]
			# 	wiki_img_folder = os.path.join(wiki_folder, 'imgs')
			# 	saveImg(img_other_url, img_file, wiki_img_folder) #_
		
			print('url parsed')

	else:
		wiki_page_data = json.loads(open(json_file_path).read()) #.strip("'<>() ")
		print('url already parsed, loaded json, url:', url_pack['url'])


	page_url_list.append(url_pack['url'])
	
	## wiki sub urls
	print('sub urls:', len(wiki_page_data['sub_url_packs']))
	for sub_url_pack in wiki_page_data['sub_url_packs']:
		if sub_url_pack['title'] == None:
			sub_url_pack['title'] == ''
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', 'wiki__' + sub_url_pack['title'].replace(' ', '_'))
		Crawl__wiki_page(sub_url_pack, sub_folder)


Crawl__wiki_page({
	'title': 'History',
	'url': wiki_history_url
}, '')

print('History Crawl done!  Layer depth:', max_depth, ' Links:', len(page_url_list), ' New images:', len(img_page_url_list))
