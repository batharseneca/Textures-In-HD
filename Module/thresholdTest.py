
import cv2
from functions import thresholdscript

from functions import GLCM

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
	
	print "Template max/min: "
	print "Max and min of p53 image: " + str(np.amax(p53)) + "," + str(np.amin(p53))

	print "Max and min of template image: " + str(np.amax(template)) + "," + str(np.amin(template))
		
	print template.dtype

	for x in range(0,template.shape[0]):
		for y in range(0,template.shape[1]):
			template[x,y] = template[x,y]/256
			p53[x,y] = p53[x,y]/256
	
	template = template.astype(np.uint8)
	p53 = p53.astype(np.uint8)

	print "Max and min of p53 (uint8) image: " + str(np.amax(p53)) + "," + str(np.amin(p53))
	print template.dtype	

	masked = thresholdscript.maskImg(template,p53)
	
	print "Max and min of masked image: " + str(np.amax(masked)) + "," + str(np.amin(masked))

	'''	
	comat = GLCM.GLCM(masked,5)
	
	print "Comat Max/Min: " + str(comat.shape)
	
	print comat
	'''
	break





exit()

