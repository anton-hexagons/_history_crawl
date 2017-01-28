import numpy as np
import urllib.request

img_url = 'https://docs.python.org/3/_static/py.png'

# file = StringIO(urllib.urlopen(URL).read())
# img = Image.open(file)

resp = urllib.request.urlopen(img_url)
image_data = np.asarray(bytearray(resp.read()), dtype="uint8")

print(image_data.shape)


# from PIL import Image
# w, h = 512, 512
# data = np.zeros((h, w, 3), dtype=np.uint8)
# data[256, 256] = [255, 0, 0]
# img = Image.fromarray(data, 'RGB')
# img.save('my.png')


from matplotlib import pyplot as plt
plt.imshow(image_data, interpolation='nearest')
plt.show()

# from scipy.misc import toimage
# toimage(image_data).show()



# import re

# prog = re.compile(r'\<h2.+\>(.+)\<\/h1\>')
# print('---')
# r = prog.findall(wiki_one)

# print(r)





# from matplotlib import pyplot as plt
# plt.imshow(image_data, interpolation='nearest')
# plt.show()