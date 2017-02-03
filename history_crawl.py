import os
import sys
import math
# import numpy
import json
import urllib.request
from html.parser import HTMLParser


# if sys.argv.length > 2:
# 	print('[depth]')
# 	exit()

wiki_history_url = '/wiki/History'
max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0
max_depth_reached = False

# img_min_res = 100

page_url_list = []
img_page_url_list = []
# img_black_list = []
url_black_list = ['#', '/wiki/Wikipedia:Protection_policy#semi', '#mw-head', '#p-search', '/wiki/List_of_national_legal_systems']
url_type_black_list = ['license']


in_content = False
img_page_urls = []
# page_imgs = []
page_sub_url_packs = []
page_thumbinner = False
# heading_title = ''
# hit_heading = False

class HTMLParser__wiki_page(HTMLParser):

	def handle_starttag(self, tag, attrs):
		global in_content
		global img_page_urls
		# global page_imgs
		global page_sub_url_packs
		global page_thumbinner
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
		if page_thumbinner and tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					img_page_url = 'https://en.wikipedia.org' + attr[1]
					img_page_urls.append(img_page_url)
			page_thumbinner = False

		# if tag == 'h1':
		# 	for attr in attrs:
		# 		if attr[0] == 'id':
		# 			if attr[1] == 'firstHeading':
		# 				hit_heading = True
		
		## page img
		# if tag == 'img':
		# 	page_img = {
		# 		'title': None,
		# 		'url': None,
		# 		'width': None,
		# 		'height': None
		# 	}
		# 	for attr in attrs:
		# 		if attr[0] == 'alt':
		# 			if attr[1]:
		# 				page_img['title'] = attr[1]
		# 		elif attr[0] == 'src':
		# 			page_img['url'] = attr[1][2:]
		# 		elif attr[0] == 'width':
		# 			page_img['width'] = int(attr[1])
		# 		elif attr[0] == 'height':
		# 			page_img['height'] = int(attr[1])
		# 	if page_img['url']:
		# 		if page_img['width'] >= img_min_res and page_img['height'] >= img_min_res:
		# 			if page_img['url'] not in img_black_list:
		# 				page_imgs.append(page_img)
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
					'title': None,
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

	# def handle_data(self, data):
	# 	global hit_heading
	# 	global heading_title
	# 	if hit_heading:
	# 		heading_title = data
	# 		hit_heading = False

	# def handle_endtag(self, tag):
	# 	pass


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
			if len(img_file) > 100:
				img_file_name = '.'.join(img_file.split('.')[:-1])
				img_file_ext = img_file.split('.')[-1]
				img_file = img_file_name[:100] + '.' + img_file_ext
				print('file name too long, cropped at 255, new file name:', img_file)
			img_file_folder = os.path.join(wiki_folder, 'imgs')
			if not os.path.exists(img_file_folder):
				os.makedirs(img_file_folder)
			img_file_path = os.path.join(img_file_folder, img_file)
			img_page_data['path'] = img_file_path
			if os.path.exists(img_file_path):
				print('img already saved')
				return
			img_data = urllib.request.urlopen('https://' + img_page_data['url']).read()
			img_file = open(img_file_path, 'wb')
			img_file.write(img_data)
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


		# ## img
		# if tag == 'img':
		# 	img = {
		# 		'title': None,
		# 		'url': None,
		# 		'width': None,
		# 		'height': None
		# 	}
		# 	rel = None
		# 	for attr in attrs:
		# 		if attr[0] == 'alt':
		# 			if attr[1]:
		# 				img['title'] = attr[1]
		# 		elif attr[0] == 'src':
		# 			img['url'] = attr[1][2:]
		# 		elif attr[0] == 'width':
		# 			img['width'] = int(attr[1])
		# 		elif attr[0] == 'height':
		# 			img['height'] = int(attr[1])
		# 	if img['url']:
		# 		if img['width'] >= 100 and img['height'] >= 100:
		# 			if img['url'] not in img_black_list:
		# 				page_imgs.append(img)

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
		'description': '',
		'info': {}
	}

	a = None
	try:
		a = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
	    print('http error:', e.code, 'url:', url)
	except urllib.error.URLError as e:
	    print('url error, url:', url)
	if a:
		wiki_img_page = str(a.read())[2:-1]
		parser = HTMLParser__wiki_img_page()
		parser.feed(wiki_img_page)

def Crawl__wiki_page(url_pack, wiki_sub_folder):
	global max_depth
	global max_depth_reached
	global img_page_urls
	# global page_imgs
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

	# if '\\\\' in url_pack['title']:
	# 	print('decode:', url_pack['title'], '<<<<<<<<<<')
	# 	exit()
	# 	#codecs.decode(title.replace('\\x', ''), 'hex').decode(encoding='UTF-8',errors='strict')

	if '/' in url_pack['title']:
		url_pack['title'] = url_pack['title'].replace('/', '__')

	
	wiki_page_data = {
		'title': url_pack['title'],
		'url': 'https://en.wikipedia.org' + url_pack['url'],
		'img_url': [],
		# 'imgs': [],
		'sub_url_packs': []
	}

	if wiki_page_data['title'] == None:
		wiki_page_data['title'] = ''

	file = 'wiki__' + wiki_page_data['title'].replace(' ', '_') + '.json'
	pyFileFolder = os.path.dirname(os.path.realpath(__file__))
	folder = os.path.join(pyFileFolder, 'wiki__History', wiki_sub_folder).replace(':', '__')
	if not os.path.exists(folder):
		os.makedirs(folder)
	wiki_folder = folder
	json_path = os.path.join(folder, file)

	if not os.path.exists(json_path):

		wiki_page = str(urllib.request.urlopen(wiki_page_data['url']).read())[2:-1]
		wiki_page_parser = HTMLParser__wiki_page()
		wiki_page_parser.feed(wiki_page)
		wiki_page_data['sub_url_packs'] = page_sub_url_packs
		# wiki_page_data['title'] = heading_title
		# heading_title = ''

		# wiki_page_data['imgs'] = page_imgs
		# for page_img in wiki_page_data['imgs']:
		# 	pass

		for img_page_url in img_page_urls:
			if img_page_url in img_page_url_list:
				print('img already saved:', img_page_url)
				break
			print('img', img_page_url)
			Crawl__wiki_img_page(img_page_url)
			img_page_data['page_url'] = img_page_url
			wiki_page_data['img_url'].append(img_page_data)

		img_page_urls = []

		with open(json_path, 'w') as outfile:
			print(json.dumps(wiki_page_data, sort_keys=False, indent=4), file=outfile)

	else:
		wiki_page_data = json.loads(open(json_path).read()) #.strip("'<>() ")
		print('url already parsed, loaded json. url:', url_pack['url'])

	page_url_list.append(url_pack['url'])
	
	print('sub urls:', len(wiki_page_data['sub_url_packs']))
	for sub_url_pack in wiki_page_data['sub_url_packs']:
		if sub_url_pack['title'] == None:
			sub_url_pack['title'] = ''
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', 'wiki__' + sub_url_pack['title'].replace(' ', '_'))
		Crawl__wiki_page(sub_url_pack, sub_folder)


Crawl__wiki_page({
	'title': 'History',
	'url': wiki_history_url
}, '')

print('History Crawl done!')
