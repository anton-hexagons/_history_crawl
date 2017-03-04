import os
import json
from PIL import Image

res = 128

hisotry_images_json_file = 'history_images.json'
hisotry_images_json = json.loads(open(hisotry_images_json_file).read())

for hisotry_image in hisotry_images_json:

	if 'path' in hisotry_image['img_pack']:

		image_path = hisotry_image['img_pack']['path']

		if os.path.exists(image_path):
	
			path_arr = hisotry_image['img_pack']['path'].split(os.sep)
			wiki_folder = os.sep.join(path_arr[:-2])
			thumb_folder = os.path.join(wiki_folder, 'thumbs')

			if not os.path.exists(thumb_folder):
				os.makedirs(thumb_folder)

			img_name = path_arr[-1]
			print('>', img_name)
			if img_name.split('.')[-1] == 'svg':
				print('skipping svg')
				continue
			img_name = ".".join(img_name.split(".")[:-1]) + "__thumb.jpg"
			thumb_path = os.path.join(thumb_folder, img_name)

			if not os.path.exists(thumb_path):

				img = Image.open(image_path)
				resize = res / max(img.size[0], img.size[1])
				size = (int(round(img.size[0] * resize)), int(round(img.size[1] * resize)))
				img.thumbnail(size)
				img.save(thumb_path)

			hisotry_image['img_pack']['thumb_path'] = thumb_path

			print('new thumb:', img_name)

			with open(hisotry_images_json_file, 'w') as outfile:
				print(json.dumps(hisotry_images_json, sort_keys=False, indent=4), file=outfile)

print('thumb creator done')