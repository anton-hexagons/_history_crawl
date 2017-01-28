print('_')

import os
# import sys
# import numpy
import urllib.request
from html.parser import HTMLParser

# if sys.argv.length > 2:
# 	print('[depth]')
# 	exit()

wiki_history_url = 'https://en.wikipedia.org/wiki/History'
depth = 3 #sys.argv[1]

img_min_res = 100

urls = []

# page_img_file_links = []
page_imgs = []
page_links = []

page_thumbinner = False

img_black_list = []
link_black_list = ['#']
link_type_black_list = ['license']

class HTMLParser__wiki_page(HTMLParser):

	def handle_starttag(self, tag, attrs):
		# global page_img_file_links
		global page_imgs
		global page_links
		global page_thumbinner

		## page img file link
		if tag == 'div':
			for attr in attrs:
				if attr[0] == 'class':
					if attr[1] == 'thumbinner':
						page_thumbinner = True
		if page_thumbinner and tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					page_img_link = 'https://en.wikipedia.org' + attr[1]
					print(page_img_link)
					page_img_file_links.append(page_img_link)
			page_thumbinner = False
		
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

		## page link
		if tag == 'a':
			page_link = {
				'title': None,
				'url': None
			}
			link_type = None
			for attr in attrs:
				if attr[0] == 'title':
					page_link['title'] = attr[1].split(' ')[-1]
				elif attr[0] == 'href':
					page_link['url'] = attr[1]
				elif attr[0] == 'rel':
					link_type = attr[1]
			if page_link['url']:
				if page_link['url'] not in link_black_list:
					if link_type not in link_type_black_list:
						page_links.append(page_link)

	def handle_endtag(self, tag):
		pass

	def handle_data(self, data):
		pass

# fullMedia = False
# # in_info_div = False
# img_data = {
# 	'org_img': {
# 		'title': None,
# 		'url': None
# 	},
# 	'info_table': None,
# 	'date': None
# }
# class HTMLParser__wiki_img_page(HTMLParser):

# 	def handle_starttag(self, tag, attrs):
# 		global fullMedia
# 		# global in_info_div
# 		## org img
# 		if tag == 'div':
# 			# class_time = None
# 			for attr in attrs:
# 				if attr[0] == 'class':
# 					if attr[1] == 'fullMedia': #fullImageLink
# 						fullMedia = True
# 					# elif attr[1] == 'hproduct commons-file-information-table':
# 					# 	in_info_div = True
# 					# elif attr[1] == 'dtstart':
# 					# 	class_time = True
# 				# elif attr[0] == 'datetime':
# 				# 	datetime = attr[1]
# 		if fullMedia and tag == 'a':
# 			for attr in attrs:
# 				if attr[0] == 'title':
# 					img_data['org_img']['titel'] = attr[1]
# 				elif attr[0] == 'href':
# 					img_data['org_img']['url'] = attr[1][2:]
# 			fullMedia = False
# 			print('::', img_data['org_img'])
# 			# imgData = urllib.request.urlopen('https://' + img_data['org_img']['url']).read()
# 			# imgFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'imgs', img_data['org_img']['url'].split('/')[-1].replace('File:', ''))
# 			# imgFile = open(imgFilePath, 'wb')
# 			# imgFile.write(imgData)
# 			# # print(type(img))
# 			return
# 		# ## img
# 		# if tag == 'img':
# 		# 	img = {
# 		# 		'title': None,
# 		# 		'url': None,
# 		# 		'width': None,
# 		# 		'height': None
# 		# 	}
# 		# 	rel = None
# 		# 	for attr in attrs:
# 		# 		if attr[0] == 'alt':
# 		# 			if attr[1]:
# 		# 				img['title'] = attr[1]
# 		# 		elif attr[0] == 'src':
# 		# 			img['url'] = attr[1][2:]
# 		# 		elif attr[0] == 'width':
# 		# 			img['width'] = int(attr[1])
# 		# 		elif attr[0] == 'height':
# 		# 			img['height'] = int(attr[1])
# 		# 	if img['url']:
# 		# 		if img['width'] >= 100 and img['height'] >= 100:
# 		# 			if img['url'] not in img_black_list:
# 		# 				page_imgs.append(img)
# 		# ## link
# 		# if tag == 'a':
# 		# 	link = {
# 		# 		'title': None,
# 		# 		'url': None
# 		# 	}
# 		# 	rel = None
# 		# 	for attr in attrs:
# 		# 		if attr[0] == 'title':
# 		# 			link['title'] = attr[1].split(' ')[-1]
# 		# 		elif attr[0] == 'href':
# 		# 			link['url'] = attr[1]
# 		# 		elif attr[0] == 'rel':
# 		# 			link['rel'] = attr[1]
# 		# 	if link['url']:
# 		# 		if link['url'] not in link_black_list and \
# 		# 			rel not in link_rel_black_list:
# 		# 			page_links.append(link)
# 		# 	#print('[link]', end='')

# 	def handle_data(self, data):
# 		global in_info_div
# 		if in_info_div:
# 			print('in_info_div:::', data)

# 	def handle_endtag(self, tag):
# 		global in_info_div
# 		if in_info_div:
# 			in_info_div = False

# def Crawl__wiki_img_page(url):
# 	wiki_img_page = str(urllib.request.urlopen(url).read())[2:-1]
# 	parser = HTMLParser__wiki_img_page()
# 	parser.feed(wiki_img_page)

def Crawl__wiki_page(url):

	if url in urls:
		return

	global page_img_file_links
	global page_imgs
	global page_links
	
	wiki_page_data = {
		'url': url,
		'img_file_links': [],
		# 'imgs': [],
		'links': []
	}

	wiki_page = str(urllib.request.urlopen(url).read())[2:-1]
	wiki_page_parser = HTMLParser__wiki_page()
	wiki_page_parser.feed(wiki_page)

	# wiki_page_data['img_file_links'] = page_img_file_links
	# # wiki_page_data['imgs'] = page_imgs
	# wiki_page_data['links'] = page_links

	# for page_img_file_link in wiki_page_data['img_file_links']:
	# 	print(page_img_file_link)
	# 	# Crawl__wiki_img_page(page_img_file_link)
	# # for page_img in wiki_page_data['imgs']:
	# # 	pass
	# for link in wiki_page_data['links']:
	# 	pass

	urls.append(url)

Crawl__wiki_page(wiki_history_url)
