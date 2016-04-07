import cv2
import numpy as np


from process import ProcessingFunctions




proc = ProcessingFunctions()


img = cv2.imread("q21notreat_xy01c2.tif", 0)


print img.shape

glcm = proc.GLCM(img, 3)

print glcm
haralick = proc.haralickALL(glcm)

print haralick




