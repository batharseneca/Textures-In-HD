import numpy as np
import cv2
import math as mt

from config import *

# All the Processing Code - Need to Ensure All Latest Versions Used # 
class ProcessingFunctions():

    def check8bitImage(self,image):
        if(image.dtype == np.dtype("uint8")):
            return True
        else:
            return False

            
    def convertTo8bit(self,image):	
        image = image.astype(np.uint8)
        return image
        
        
    
    def GLCM(self,Img,nhood):
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
 
 
 
    def haralickALL(self,CoMat):
        outputFeatures =[
            self.ASM(CoMat),
            self.contrast(CoMat),
            self.IDM(CoMat),
            self.entropy(CoMat),
            self.xmean(CoMat),
            self.ymean(CoMat),
            self.xstdev(CoMat),
            self.ystdev(CoMat),
            self.CORR(CoMat),
            self.mean(CoMat),
            self.variance(CoMat),
            self.sumAverage(CoMat),
            self.sumEntropy(CoMat),
            self.difEntropy(CoMat),
            self.inertia(CoMat),
            self.clusterShade(CoMat),
            self.clusterProm(CoMat),
        ]
        return outputFeatures


    ## Angular Second Moment(ASM) / Energy is a measure of homogeneity in an image
    def ASM(self,CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j])**2
        return val
	
    ## Contrast adds the comatrival, but favours when values are away from the diagonal
    def contrast(self,CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * (abs(i-j)**2)
        return val

    ## Local homogeneity (Inverse Difference Moment)
    def IDM(self,CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * 1/(1+(i-j)**2)
        return val
        
    ## Entropy (Log function had to have a +1 to ensure that values are not zero)
    def entropy(self,CoMat):
        val=0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (CoMat[i][j]) * mt.log(CoMat[i][j]+1)
        return val * (-1)

    ## Horizontal Mean
    def xmean(self,CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += i * CoMat[i][j]
        return val

    ## Vertical Mean
    def ymean(self,CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += j * CoMat[i][j]
        return val

    ## Horizontal Standard Deviation
    def xstdev(self,CoMat):
        val = 0
        xmeanVal = self.xmean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i-xmeanVal)**2) * CoMat[i][j]
        return val	
            
    # Vertical Standard Deviation	
    def ystdev(self,CoMat):
        val = 0
        ymeanVal = self.ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((j-ymeanVal)**2) * CoMat[i][j]
        return val

    ## The actual correlation function, requires the above calculations
    def CORR(self,CoMat):
        val = 0
        xmeanVal = self.xmean(CoMat)
        ymeanVal = self.ymean(CoMat)
        
        xStdVal = self.xstdev(CoMat)
        yStdVal = self.ystdev(CoMat)
    
        if(xStdVal * yStdVal == 0):
            return 0

        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i*j) * CoMat[i][j] - (xmeanVal-ymeanVal))/(xStdVal*yStdVal)
        return val	

    # Total Mean
    def mean(self,CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += CoMat[i][j]
        num = CoMat.shape[0] * CoMat.shape[1]
        mean = val / num
        return mean

    # Sum of Squares, Variance
    def variance(self,CoMat):
        val = 0
        meanVal = self.mean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i-meanVal)**2 * CoMat[i][j]
        return val

    # P(x+y) is the diagonal sum of the matrix.
    def xPlusY(self,CoMat,kValue):
        val = 0
        if(kValue < CoMat.shape[0]):
            i=kValue
            j=0
            while(i!=0):
                val += CoMat[i][j]
                i -= 1
                j += 1
            return val
        if(kValue >= CoMat.shape[0]):
            i=CoMat.shape[0]-1
            j= kValue - CoMat.shape[0]-1
            while(j != CoMat.shape[0]):
                val += CoMat[i][j]
                i -= 1
                j += 1
            return val

    # Sum Average	
    def sumAverage(self,CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]*2-2):
            val += self.xPlusY(CoMat,k) * k
        return val

    # Sum Entropy (Log function had to have a +1 to ensure that values are not zero)
    def sumEntropy(self,CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]*2-2):
            val += self.xPlusY(CoMat,k)* mt.log(self.xPlusY(CoMat,k)+1)
        return val*(-1)
        
    # Differencce Entropy (Log function had to have a +1 to ensure that values are not zero)
    def difEntropy(self,CoMat):
        val = 0
        for k in range(0,CoMat.shape[0]-1):
            val += self.xPlusY(CoMat,k)* mt.log(self.xPlusY(CoMat,k)+1)
        return val*(-1)

    # Inertia
    def inertia(self,CoMat):
        val = 0
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += ((i-j)**2) * CoMat[i][j]
        return val
       
    # Cluster Shade
    def clusterShade(self,CoMat):
        val = 0
        ux = self.xmean(CoMat)
        uy = self.ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i + j - ux - uy)**3 * CoMat[i][j]
        return val        

    # Cluster Prominance
    def clusterProm(self,CoMat):
        val = 0
        ux = self.xmean(CoMat)
        uy = self.ymean(CoMat)
        for i in range(0,CoMat.shape[0]-1):
            for j in range(0,CoMat.shape[1]-1):
                val += (i + j - ux - uy)**4 * CoMat[i][j]
        return val
    
