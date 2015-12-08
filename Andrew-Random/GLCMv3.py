import numpy as np
from numba import jit


'''Version 3 of GLCM function. It takes an image and returns the normalized gray level co-occurance matrix. Requires numpy module imported as 'np'.
For speed it makes use of jit imported from the 'numba' module, this can be removed, will slow the funciton down however. Although longer, it 
is much faster, no looping all vectorized. '''


@jit
def GLCM(Img,nhood):

    CoMatDim=(np.amax(Img)+1,np.amax(Img)+1) 
    CoMat=np.zeros(CoMatDim,dtype=np.int) #Initialize CoMat as matrix of zeros

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


    CoMat=np.divide(CoMat,np.sum(CoMat)) #Normalize CoMat#
    
    return(CoMat)


