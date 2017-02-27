#!/usr/bin/env python

from PIL import Image

im = Image.open("test.jpg")
resize = 128 / max(im.size[0], im.size[1])
size = (int(round(im.size[0] * resize)), int(round(im.size[1] * resize)))
im.thumbnail(size)
im.save("test_tumb.jpg")

# import os, sys

# def resizeImage(infile, output_dir="", size=(1024,768)):
#      outfile = os.path.splitext(infile)[0]+"_resized"
#      extension = os.path.splitext(infile)[1]

#      if infile != outfile:
#         try :
#             im = Image.open(infile)
#             im.thumbnail(size, Image.ANTIALIAS)
#             im.save(output_dir+outfile+extension,"JPEG")
#         except IOError:
#             print("cannot reduce image for ", infile, "error:", IOError)


# if __name__=="__main__":
#     output_dir = "resized"
#     dir = os.getcwd()

#     if not os.path.exists(os.path.join(dir,output_dir)):
#         os.mkdir(output_dir)

#     #for file in os.listdir(dir):
#    resizeImage(os.path.join(dir,"test.png"),output_dir)