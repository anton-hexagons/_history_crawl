import os
import sys
import math
import json
import urllib.request
import requests


hisotry_images_json_file = 'history_images.json'
hisotry_images_json = json.loads(open(hisotry_images_json_file).read().strip("'<>"))

max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 0
max_depth_reached = False

img_count = 0


def Collector_crawl(wiki_sub_folder):

	global max_depth
	global max_depth_reached
	global img_count


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


	if 'collected' in wiki_json and wiki_json['collected']:
		print('>> collected, wiki:', wiki_json['title'], ' wiki_sub_folder:', wiki_sub_folder)

	else:

		if 'location_searched' not in wiki_json:
			print('>> location not searched, wiki:', wiki_json['title'], ' wiki_sub_folder:', wiki_sub_folder)

		else:

			print('>> wiki:', wiki_json['title'], ' wiki_sub_folder:', wiki_sub_folder)

			if 'img_packs' in wiki_json:
				for img_pack in wiki_json['img_packs']:

					img_location = None

					if 'path' in img_pack:

						img_name__location = img_pack['img_name_location']
						no_location = img_name__location == None or isinstance(img_name__location, str)
						if not no_location:
							img_location = img_name__location

					if not img_location and 'img_caption' in img_pack:

						img_caption__location = img_pack['img_caption_location']
						no_location = img_caption__location == None or isinstance(img_caption__location, str)
						if not no_location:
							img_location = img_caption__location

					for info in img_pack['info']:
						if not img_location and 'Current location' in info:
							
							current_location__location = img_pack['img_current_location']
							img_location = current_location__location
							
					img_info = {
						'img_pack': img_pack,
						'location': img_location,
						'json_path': wiki_json_file
					}

					hisotry_images_json.append(img_info)

					with open(hisotry_images_json_file, 'w') as outfile:
						print(json.dumps(hisotry_images_json, sort_keys=False, indent=4), file=outfile)

					img_count += 1

			wiki_json['collected'] = True

			with open(wiki_json_file, 'w') as outfile:
				print(json.dumps(wiki_json, sort_keys=False, indent=4), file=outfile)
				

	for sub_url_pack in wiki_json['sub_url_packs']:
		title = sub_url_pack['title']
		if title == None:
			title = ''
		sub_folder = os.path.join(wiki_sub_folder, 'sub_wikis', 'wiki__' + title.replace(' ', '_'))
		Collector_crawl(sub_folder)


Collector_crawl('wiki__History')


print('Collector Crawl done!  Layer depth:', max_depth, ' Found', str(img_count), 'images.')
