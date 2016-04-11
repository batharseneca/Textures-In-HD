# This script proceesses all the information in the p-53 sample
# Reads in the hoechst and p-53 channel


import cv2
import numpy as np
import skimage


import csv

hoechst = []
p53 = []

from scipy import misc
import scipy as sp
from skimage import img_as_ubyte

from matplotlib import pyplot as plt

from skimage import exposure
import os
with open("/mnt/B4C2E08EC2E05660/Users/Nishanth/Documents/IGPProject/ImageAnalysis-IGP/dataMunging/formatting.csv", "rb") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ")
        for row in spamreader:
            line = (",".join(row)).split(",")
            hoechst.append(line[0])
            p53.append(line[-1])


for i in range(0,len(hoechst)):
    
    hList = hoechst[i].split(os.path.sep)
    pList = p53[i].split(os.path.sep)

    hList.insert(6, "normalized")
    pList.insert(6, "normalized")
    pList[-2] = "p53"


    hPath = os.path.sep.join(hList)
    pPath = os.path.sep.join(pList)

    hImage = cv2.imread(hPath,0)
    pImage = cv2.imread(pPath,0)


    ret, mask = cv2.threshold(hImage,245,255,cv2.THRESH_BINARY)

    pImage_thresh = pImage * (mask !=0)


    pList[7] = "masked"

    maskedPath = os.path.sep.join(pList)
    
    cv2.imwrite(maskedPath,pImage_thresh)
    print str(i) + " out of " + str(len(hoechst)) + " done!"
    




exit()



print len(hoechst)
print len(p53)




hoechstPath = "/mnt/B4C2E08EC2E05660/Users/Nishanth/Documents/IGPProject/data/normalized/hoechst"
p53Path = "/mnt/B4C2E08EC2E05660/Users/Nishanth/Documents/IGPProject/data/normalized/p53"

for i in range(0,len(hoechst)):
    hoe_image = sp.misc.imread(hoechst[i],0)
    p53_image = sp.misc.imread(p53[i],0)

    hoe_norm = exposure.equalize_hist(hoe_image)
    p53_norm = exposure.equalize_hist(p53_image)

    hName = hoechstPath + os.path.sep + hoechst[i].split(os.path.sep)[-1]
    pName = p53Path + os.path.sep + p53[i].split(os.path.sep)[-1]

    sp.misc.imsave(hName,hoe_norm)
    sp.misc.imsave(pName,p53_norm)


    


