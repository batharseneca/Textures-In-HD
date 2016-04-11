from process_V3 import *
import numpy as np

image = np.array([[0, 0, 1, 1],
                  [0, 0, 1, 1],
                  [0, 2, 0, 2],
                  [2, 2, 3, 3]], dtype=np.uint8)



processing = ProcessingFunctions()
'''

print image



coMat = processing.GLCM(image, 1)

print coMat[ : , : , 0, 0 ]


print np.delete(coMat[:,:,0,0] ,(0),axis=0)
'''

import cv2
realImage = cv2.imread("q21notreat_xy01c2.tif",0)

realComat = processing.GLCM(realImage,5)

'''
realComat = np.zeros((256,256),dtype=np.int)
for i in range(0,3):
    realComat += CoMat2[:,:,0,i]
'''
print realComat.shape
print realComat
