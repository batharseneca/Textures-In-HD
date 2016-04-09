import numpy as np
import cv2
import time
from skimage import img_as_ubyte


image = "q21notreat_xy03c2.tif" 
img1 = cv2.imread(image,0)
img = img_as_ubyte(img1) #tried it with and without this
timeset = []

def GLCM(Img,nhood):
    print "DOUBLE CHECK: " 
    print nhood
    
    print "\n\n\n"
    CoMatDim=(np.amax(Img)+1,np.amax(Img)+1) 
    CoMat=np.zeros(CoMatDim,dtype=np.uint) #Initialize CoMat as matrix of zeros

    #First Direction
    ImgCopy1RowKeep=np.arange(nhood,Img.shape[0])
    ImgCopy2RowKeep=np.arange(0,Img.shape[0]-nhood)
    ImgCopy1=Img[ImgCopy1RowKeep,:]
    ImgCopy2=Img[ImgCopy2RowKeep,:]

    ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
    ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
    ImgCopy1=ImgCopy1[:,ImgCopy1ColKeep]
    ImgCopy2=ImgCopy2[:,ImgCopy2ColKeep]

    ImgFlat1=np.ndarray.flatten(ImgCopy1)
    ImgFlat2=np.ndarray.flatten(ImgCopy2)


    for d in range(0,ImgFlat1.shape[0]):
        CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

    #Second Direction
    ImgCopy1RowKeep=np.arange(nhood,Img.shape[0])
    ImgCopy2RowKeep=np.arange(0,Img.shape[0]-nhood)
    ImgCopy1=Img[ImgCopy1RowKeep,:]
    ImgCopy2=Img[ImgCopy2RowKeep,:]

    ImgFlat1=np.ndarray.flatten(ImgCopy1)
    ImgFlat2=np.ndarray.flatten(ImgCopy2)

    for d in range(0,ImgFlat1.shape[0]):
        CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

    #Third Direction
    ImgCopy1RowKeep=np.arange(0,Img.shape[0]-nhood)
    ImgCopy2RowKeep=np.arange(nhood,Img.shape[0])
    ImgCopy1=Img[ImgCopy1RowKeep,:]
    ImgCopy2=Img[ImgCopy2RowKeep,:]

    ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
    ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
    ImgCopy1=ImgCopy1[:,ImgCopy1ColKeep]
    ImgCopy2=ImgCopy2[:,ImgCopy2ColKeep]

    ImgFlat1=np.ndarray.flatten(ImgCopy1)
    ImgFlat2=np.ndarray.flatten(ImgCopy2)

    for d in range(0,ImgFlat1.shape[0]):
        CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

    #Fourth Direction
    ImgCopy1ColKeep=np.arange(nhood,Img.shape[1])
    ImgCopy2ColKeep=np.arange(0,Img.shape[1]-nhood)
    ImgCopy1=Img[:,ImgCopy1ColKeep]
    ImgCopy2=Img[:,ImgCopy2ColKeep]

    ImgFlat1=np.ndarray.flatten(ImgCopy1)
    ImgFlat2=np.ndarray.flatten(ImgCopy2)

    for d in range(0,ImgFlat1.shape[0]):
        CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1

    CoMat = np.delete(CoMat,(0),axis=0)
    CoMat = np.delete(CoMat,(0),axis=1) 

    CoMat = CoMat.astype(np.float_)
    
    CoMat=np.divide(CoMat,np.sum(CoMat)) #Normalize CoMat#
    
    return CoMat

tic = time.clock() 
holder = GLCM(img,1)
toc = time.clock()
zime = toc - tic
timeset.append(zime) 
print "---------0 complete-----1--" + str(zime) 


tic = time.clock() 
holder = GLCM(img,5)
toc = time.clock()
zime = toc - tic
timeset.append(zime) 
print "---------1 complete-----5--:" + str(zime) 


tic = time.clock() 
holder = GLCM(img,20)
toc = time.clock()
zime = toc - tic
timeset.append(zime) 
print "---------2 complete-----20--:" + str(zime) 



tic = time.clock() 
holder = GLCM(img,90)
toc = time.clock()
zime = toc - tic
timeset.append(zime) 
print "---------3 complete-----90--:" + str(zime)



tic = time.clock() 
holder = GLCM(img,900)
toc = time.clock()
zime = toc - tic
timeset.append(zime) 
print "---------4 complete-----900--:" + str(zime) 


print timeset  



                                             ##OUTPUT Without Compression Using 8bit:
                                             
                                             # C:\Users\Bilal Athar\Desktop\Bilal_Test\ImageAnalysis-IGP\final>python GLCMtest.py
                                            # DOUBLE CHECK:
                                            # 1




                                            # ---------0 complete-----1--59.7227882691
                                            
                                            
                                            
                                            # DOUBLE CHECK:
                                            # 5




                                            # ---------1 complete-----5--:59.3178110193
                                            
                                            
                                            
                                            # DOUBLE CHECK:
                                            # 20




                                            # ---------2 complete-----20--:58.9059693642
                                            
                                            
                                            # DOUBLE CHECK:
                                            # 90




                                            # ---------3 complete-----90--:55.9188044166
                                            
                                            # DOUBLE CHECK:
                                            # 900




                                            # ---------4 complete-----900--:26.1276607482
                                           
                                           # nhood sizes: [1,5,20,90,900]
                                           # times:       [59.72278826910247, 59.317811019312025, 58.905969364191506, 55.91880441661962, 26.12766074819109]

                                           ##OUTPUT With Compression Using 8bit:
                                           
                                            # C:\Users\Bilal Athar\Desktop\Bilal_Test\ImageAnalysis-IGP\final>python GLCMtest.py
                                            # DOUBLE CHECK:
                                            # 1




                                            # ---------0 complete-----1--60.5378765331
                                            # DOUBLE CHECK:
                                            # 5




                                            # ---------1 complete-----5--:60.4245650947
                                            # DOUBLE CHECK:
                                            # 20




                                            # ---------2 complete-----20--:59.6999024991
                                            # DOUBLE CHECK:
                                            # 90




                                            # ---------3 complete-----90--:56.3320157883
                                            # DOUBLE CHECK:
                                            # 900




                                            # ---------4 complete-----900--:26.2223713245
                                            # nhood sizes: [1,5,20,90,900]
                                            # times:       [60.53787653307333, 60.4245650946785, 59.69990249910197, 56.33201578830332, 26.22237132447276]