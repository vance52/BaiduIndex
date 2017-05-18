# -*- coding:utf-8 -*-
import Image
import os

file_list = os.listdir('numbers')
for ff in file_list:
	tmpf = Image.open("numbers/%s" % ff)
	fh=open("text/%s" % ff.split('.')[0], 'w')
	width=tmpf.size[0]
	height=tmpf.size[1]
	for i in range(0,width):
		for j in range(0,height):
			cl=tmpf.getpixel((i,j))
			clall=cl[0]+cl[1]+cl[2]
			if(clall==231):
				#黑色
				fh.write("1")
			else:
				fh.write("0")
		fh.write("\n")
	fh.close()
