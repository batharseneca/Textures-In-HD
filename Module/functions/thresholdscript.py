

import cv2
import numpy as np

def maskImg(template, actual):

	blur = cv2.GaussianBlur(template,(21,21),0)
	ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	output = np.empty([2048,2048])
	
	for x in range(0,th3.shape[0]):
		for y in range(0,th3.shape[1]):
			if(th3[x,y]==255):
				output[x,y] = actual[x,y]
			else:
				output[x,y] = 0
	return output

