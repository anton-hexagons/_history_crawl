import os
import sys
import math
import json”
import urllib.request


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

		if map_status == 'OK':

			map_result = map_json['results'][0]

			map_pack = {
				'name': map_result['address_components'][0]['long_name'],
				'id': map_result['place_id'],
				'address': map_result['formatted_address'],
				'location': map_result['geometry']['location'],
				'accuracy': map_result['geometry']['location_type']
			}

			return map_pack

		else:

			return None


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
	wiki_json = json.loads(open(wiki_json_file).read())

	print('> wiki:', wiki_json['title'])


	if 'img_packs' in wiki_json:
		for img_pack in wiki_json['img_packs']:
			if 'img_caption' in img_pack:
				if 'img_caption_location' in img_pack:
					if img_pack['img_caption_location'] == 'private_collection':
						print('img_caption_location already found, title:', img_pack['img_caption'], ', location: private_collection')
					else:
						print('img_caption_location already found, title:', img_pack['img_caption'], ', location:', img_pack['img_caption_location']['location'], img_pack['img_caption_location']['accuracy'])
				else:
					img_caption__location_pack = Seach_map(img_pack['img_caption'])
					if img_caption__location_pack:
						if img_caption__location_pack == 'private_collection':
							print('img_caption_location, title:', img_pack['img_caption'], ', location: private_collection')
						else:
							print('img_caption_location, title:', img_pack['img_caption'], ', location:', img_caption__location_pack['location'], img_caption__location_pack['accuracy'])
						img_pack['img_caption_location'] = img_caption__location_pack
						img_location_count += 1
			else:
				pass
				# print('no img_caption')
			for info in img_pack['info']:
				if 'Current location' in info:
					if 'img_current_location' in img_pack:
						if img_pack['img_current_location'] == 'private_collection':
							print('current_location already found, title:', img_pack['img_caption'], ', location: private_collection')
						else:
							print('current_location already found, title:', current_location, ', location:', img_pack['img_current_location']['location'], img_pack['img_current_location']['accuracy'])
					else:
						current_location = img_pack['info'][info]
						current_location__location_pack = Seach_map(current_location)
						if current_location__location_pack:
							if current_location__location_pack == 'private_collection':
								print('current_location, title:', current_location, ', location: private_collection')
							else:
								print('current_location, title:', current_location, ', location:', current_location__location_pack['location'], current_location__location_pack['accuracy'])
							img_pack['img_current_location'] = current_location__location_pack
							img_location_count += 1
			img_count += 1
	else:
		pass
		# print('no img_packs')

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
