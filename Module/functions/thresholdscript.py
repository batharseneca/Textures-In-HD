




# sys.path.append('c:\users\nishanth\miniconda3\lib\site-packages')
# import cv2


# from PIL import Image
import numpy as np



import cv2

print(cv2.__version__)

exit()




img = cv2.imread('TESTIMG.tif',0)
ret, th2 = cv2.threshold(img,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
imarray = numpy.array(th2)

mg = Image.fromarray(imarray)
mg.save("sampleOUTPUT2.tif")