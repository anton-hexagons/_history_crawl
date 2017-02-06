import os
import sys
import math
import json
import urllib.request


max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0
max_depth_reached = False

img_count = 0

# location = 'Obelisk Luxor' #'Stockholm'
# map_url = 'https://maps.googleapis.com/maps/api/geocode/json?&address=' + location + '&key=AIzaSyBl08GvP1rUEmPOpPHcPZ2WJhvwjuGlxpg'

# map_page = urllib.request.urlopen(map_url).read()
# map_json = json.loads(map_page)
# map_status = map_json['status']

# if map_status == 'OK':

# 	map_result = map_json['results'][0]
# 	map_result_name = map_result['address_components'][0]['long_name']
# 	map_result_id = map_result['place_id']
# 	map_result_address = map_result['formatted_address']
# 	map_result_coordinate = map_result['geometry']['location']
# 	map_result_accuracy = map_result['geometry']['location_type']

# 	print('map_result_name:', map_result_name)
# 	print('map_result_address:', map_result_address)
# 	print('map_result_coordinate:', map_result_coordinate)
# 	print('map_result_accuracy:', map_result_accuracy)


def Map_crawl(wiki_sub_folder):

	global max_depth
	global max_depth_reached
	global img_count


	sub_wiki_depth = math.ceil((wiki_sub_folder.count(os.sep)) / 2)
	if sub_wiki_depth > max_depth:
		if not max_depth_reached:
			print('> max depth reached.')
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
				print('img_caption:', img_pack['img_caption'])
				img_count += 1
			else:
				print('no img_caption')
	else:
		print('no img_packs')

	for sub_url_pack in wiki_json['sub_url_packs']:
		title = sub_url_pack['title']
		if title == None:
			title = ''
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', 'wiki__' + title.replace(' ', '_'))
		Map_crawl(sub_folder)


Map_crawl('wiki__History')


print('Map Crawl done!  Layer depth:', max_depth)
