
import numpy as np

def check8bitImage(image):
	if(image.dtype == np.dtype("uint8")):
		return True
	else:
		return False




def convertTo8bit(image):
	
	image //= 256
	image = image.astype(np.uint8)
	return image


