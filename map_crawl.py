import os
import sys
import math
import json
import urllib.request
import requests


map_key = 'AIzaSyBl08GvP1rUEmPOpPHcPZ2WJhvwjuGlxpg'

max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0
max_depth_reached = False

img_count = 0
img_location_count = 0

# location_backlist = []


def Seach_map(location):

	# if location in location_backlist:
	# 	print('location blacklisted:', location)
	# 	return None

	if location == '\\nPrivate collection':
		return 'private_collection'
	
	location = location.replace('\\n', '')
	location = location.replace(' ', '%20')
	location = str(location.encode('utf-8').strip())
	
	map_url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=' + location + '&key=' + map_key

	a = None
	try:
		a = urllib.request.urlopen(map_url)
	except urllib.error.HTTPError as e:
		print('http error:', e.code, 'url:', map_url)
		return None
	except urllib.error.URLError as e:
		print('url error, url:', map_url)
		return None
	if a:
		map_page = a.read()
		map_json = json.loads(map_page)
		map_status = map_json['status']

		if map_status == 'OK' or map_status in ['ROOFTOP']:

			map_result = map_json['results'][0]

			map_pack = {
				'name': map_result['address_components'][0]['long_name'],
				'id': map_result['place_id'],
				'address': map_result['formatted_address'],
				'location': map_result['geometry']['location'],
				'accuracy': map_result['geometry']['location_type']
			}
			# print('map_status: OK  location:', map_pack['name'])
			return map_pack

		elif map_status == 'ZERO_RESULTS':
			return None

		else:
			print('location:', location, ' map_status:', map_status)


def Map_crawl(wiki_sub_folder):

	global max_depth
	global max_depth_reached
	global img_count
	global img_location_count


	sub_wiki_depth = math.ceil((wiki_sub_folder.count(os.sep)) / 2)
	if sub_wiki_depth > max_depth:
		if not max_depth_reached:
			# print('> max depth reached.')
			max_depth_reached = True
		return
	elif max_depth_reached:
		max_depth_reached = False


	current_folder = os.path.dirname(os.path.realpath(__file__))
	wiki_json_name = wiki_sub_folder.split(os.sep)[-1] + '.json'
	wiki_json_file = os.path.join(current_folder, wiki_sub_folder, wiki_json_name)
	if not os.path.exists(wiki_json_file):
		print('json dose not exist:', wiki_json_name)
		return
	wiki_json = json.loads(open(wiki_json_file).read().strip("'<>"))


	if 'location_searched' in wiki_json and wiki_json['location_searched']:
		print('>> location_searched wiki:', wiki_json['title'], ' wiki_sub_folder:', wiki_sub_folder)

	else:

		print('>> wiki:', wiki_json['title'], ' wiki_sub_folder:', wiki_sub_folder)

		if 'img_packs' in wiki_json:
			for img_pack in wiki_json['img_packs']:

				if 'path' in img_pack:

					location_title = '.'.join(os.path.basename(img_pack['path']).split('.')[:-1])

					checked = 'img_name_location' in img_pack
					if checked:
						img_name__location = img_pack['img_name_location']
					else:
						img_name__location = Seach_map(location_title)
						img_pack['img_name_location'] = img_name__location

					no_location = img_name__location == None or isinstance(img_name__location, str)

					print(
						'old,' if checked else ('none,' if no_location else '> new,'),
						'img_name_location,',
						'title: [', location_title, ']',
						'location:', img_name__location if no_location else img_name__location['name'],
						'' if no_location else img_name__location['location'],
						'' if no_location else img_name__location['accuracy']
					)
				
					if not checked and not no_location:
						img_location_count += 1


				if 'img_caption' in img_pack:

					location_title = img_pack['img_caption']

					checked = 'img_caption_location' in img_pack
					if checked:
						img_caption__location = img_pack['img_caption_location']
					else:
						img_caption__location = Seach_map(location_title)
						img_pack['img_caption_location'] = img_caption__location
					
					no_location = img_caption__location == None or isinstance(img_caption__location, str)

					print(
						'old,' if checked else ('none,' if no_location else '> new,'),
						'img_caption_location,',
						'title: [', location_title, ']',
						'location:', img_caption__location if no_location else img_caption__location['name'],
						'' if no_location else img_caption__location['location'],
						'' if no_location else img_caption__location['accuracy']
					)
				
					if not checked and not no_location:
						img_location_count += 1


				for info in img_pack['info']:
					if 'Current location' in info:
						
						location_title = img_pack['info'][info]

						checked = 'img_current_location' in img_pack
						if checked:
							current_location__location = img_pack['img_current_location']
						else:
							current_location__location = Seach_map(location_title)
							img_pack['img_current_location'] = current_location__location

						no_location = current_location__location == None or isinstance(img_pack['img_current_location'], str)

						print(
							'old,' if checked else ('none,' if no_location else '> new,'),
							'img_current_location,',
							'title: [', location_title, ']',
							'location:', current_location__location if no_location else current_location__location['name'],
							'' if no_location else current_location__location['location'],
							'' if no_location else current_location__location['accuracy']
						)

						if not checked and not no_location:
							img_location_count += 1
				

				img_count += 1

		wiki_json['location_searched'] = True

		with open(wiki_json_file, 'w') as outfile:
			print(json.dumps(wiki_json, sort_keys=False, indent=4), file=outfile)
				

	for sub_url_pack in wiki_json['sub_url_packs']:
		title = sub_url_pack['title']
		if title == None:
			title = ''
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', 'wiki__' + title.replace(' ', '_'))
		Map_crawl(sub_folder)


Map_crawl('wiki__History')


print('Map Crawl done!  Layer depth:', max_depth, ' Found', str(img_location_count), 'locations in', str(img_count), 'images.')
