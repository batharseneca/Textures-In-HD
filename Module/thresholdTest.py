
import cv2
from functions import thresholdscript

import os

import numpy as np

import scipy as sp
import scipy.misc

import matplotlib

from matplotlib import pyplot as plt

matplotlib.get_backend()


f = open("/home/nmerwin/Documents/IGPProject/ImageAnalysis-IGP/dataMunging/formatting.csv","r")

for line in f:
	
	lineArray = line.rstrip().split(",");
	print lineArray
	
	template = sp.misc.imread(lineArray[0])
	
	p53 = sp.misc.imread(lineArray[4])
	
	print "Template and p53 image sizes are: " +  str(template.shape) +str(p53.shape)
	
	print template.dtype

	for x in range(0,template.shape[0]):
		for y in range(0,template.shape[1]):
			template[x,y] = template[x,y]/256
			p53[x,y] = p53[x,y]/256
	
	template = template.astype(np.uint8)
	p53 = p53.astype(np.uint8)

	print template.dtype	

	masked = thresholdscript.maskImg(template,p53)
	
	plt.imshow(template,"gray")
	plt.savefig("template.png")	

	plt.imshow(p53,"gray")
	plt.savefig("p53.png")
	
	
	plt.imshow(masked,'gray')
	plt.savefig("masked.png")
	
	break




exit()


'''

for i in range(2,len(hoechstDir)):
	print "Max and min of template are: " + str(np.amax(template)) + ',' + str(np.amin(template))
	print "Max and min of actual are: " + str(np.amax(actual)) + ',' + str(np.amin(actual))
	print "Data type is: " + str(type(template))
	
	template8bit = np.empty([template.shape[0],template.shape[1]])
	
	for x in range(0,template.shape[0]):
		for y in range(0,template.shape[1]):
			template8bit[np.array([x]), np.array([y])] = template[np.array([x]), np.array([y])]/256
	
	print template8bit	


	for x in range(0,len(template.ravel())):
		template8bit.append(template.ravel()[x]/256)
	print template8bit.shape

	# template8bit = np.reshape(template8bit,(template.shape[0],template.shape[1]))
	# print "Shape of original: " , str(template.shape())# + "Shape of modified: " + str(template8bit.shape())
	
	
	
	
	# maske = thresholdscript.maskImg(template,actual)

# print os.path.abspath(hoechstDir[0])

print "THIS FUCKING WORKS"
'''



