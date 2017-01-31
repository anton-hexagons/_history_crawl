import os
import sys
# import numpy
import json
import urllib.request
from html.parser import HTMLParser

# if sys.argv.length > 2:
# 	print('[depth]')
# 	exit()

wiki_history_url = 'https://en.wikipedia.org/wiki/History'
max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# img_min_res = 100

urls = []
# img_black_list = []
url_black_list = ['#']
url_type_black_list = ['license']


img_page_urls = []
# page_imgs = []
page_sub_url_packs = []
page_thumbinner = False
# heading_title = ''
# hit_heading = False

class HTMLParser__wiki_page(HTMLParser):

	def handle_starttag(self, tag, attrs):
		global img_page_urls
		# global page_imgs
		global page_sub_url_packs
		global page_thumbinner
		global hit_heading

		## page imgs from thumbinners
		if tag == 'div':
			for attr in attrs:
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

		## page url
		if tag == 'a':
			page_url_pack = {
				'title': None,
				'url': None
			}
			url_type = None
			for attr in attrs:
				if attr[0] == 'title':
					page_url_pack['title'] = attr[1].split(' ')[-1]
				elif attr[0] == 'href':
					page_url_pack['url'] = attr[1]
				elif attr[0] == 'rel':
					url_type = attr[1]
			if page_url_pack['url']:
				if page_url_pack['url'] not in url_black_list:
					if url_type not in url_type_black_list:
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
			img_data = urllib.request.urlopen('https://' + img_page_data['url']).read()
			img_file = img_page_data['url'].split('/')[-1].replace('File:', '')
			img_file_folder = os.path.join(wiki_folder, 'imgs')
			if not os.path.exists(img_file_folder):
				os.makedirs(img_file_folder)
			img_file_path = os.path.join(img_file_folder, img_file)
			img_page_data['path'] = img_file_path
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

	wiki_img_page = str(urllib.request.urlopen(url).read())[2:-1]

	parser = HTMLParser__wiki_img_page()
	parser.feed(wiki_img_page)

def Crawl__wiki_page(url_pack, wiki_sub_folder):
	global img_page_urls
	# global page_imgs
	global page_sub_url_packs
	global img_page_data
	global heading_title
	global wiki_folder


	sub_wiki_depth = (wiki_sub_folder.count(os.sep) - 1) / 2
	if sub_wiki_depth > max_depth:
		print('max depth reached')
		return

	if url_pack['url'] in urls:
		print(url_pack, "- url already visited")
		return
	else:
		print(url_pack)
	
	wiki_page_data = {
		'title': url_pack['title'],
		'url': url_pack['url'],
		'img_url': [],
		# 'imgs': [],
		'sub_url_packs': []
	}

	wiki_page = str(urllib.request.urlopen(url_pack['url']).read())[2:-1]
	wiki_page_parser = HTMLParser__wiki_page()
	wiki_page_parser.feed(wiki_page)
	wiki_page_data['sub_url_packs'] = page_sub_url_packs
	# wiki_page_data['title'] = heading_title
	# heading_title = ''

	# wiki_page_data['imgs'] = page_imgs

	file = 'wiki_' + wiki_page_data['title'].replace(' ', '_') + '.json'
	pyFileFolder = os.path.dirname(os.path.realpath(__file__))
	folder = os.path.join(pyFileFolder, 'wiki', wiki_sub_folder)
	print('---', os.path.exists(folder))
	if not os.path.exists(folder):
		os.makedirs(folder)
	wiki_folder = folder
	path = os.path.join(folder, file)

	for img_page_url in img_page_urls:
		Crawl__wiki_img_page(img_page_url)
		img_page_data['page_url'] = img_page_url
		wiki_page_data['img_url'].append(img_page_data)

	with open(path, 'w') as outfile:
		print(json.dumps(wiki_page_data, sort_keys=False, indent=4), file=outfile)

	# for page_img in wiki_page_data['imgs']:
	# 	pass

	for sub_url_pack in wiki_page_data['sub_url_packs']:
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', url_pack['title'].replace(' ', '_'))
		pass

	urls.append(url_pack['url'])

Crawl__wiki_page({
	'title': 'History',
	'url': wiki_history_url
}, os.sep)
