import numpy as np
import cv2
import math as mt

from skimage import img_as_ubyte

from skimage.feature import greycomatrix

# All the Processing Code - Need to Ensure All Latest Versions Used # 
class ProcessingFunctions():

    def isImage(self,image):
        if(img.dtype):
            return True
        else:
            return False
      

    def check8bitImage(self,image):
        if(image.dtype == np.dtype("uint8")):
            return True
        else:
            return False

            
    def convertTo8bit(self,image):
        image = img_as_ubyte(image)  
        #image = image.astype(np.uint8)
        return image
        
        
    
    def GLCM(self,Img,nhood):
        # Using the skimage package
        CoMat4D = greycomatrix(Img, angles= [0, np.pi/2, np.pi, 3*np.pi/2], distances = [nhood], levels=256)
        # Sum accross all directions
        CoMat = np.zeros((256,256),dtype=np.int)
        for i in range(0,3):
            CoMat += CoMat4D[:,:,0,i]
        # Remove 0,0 axes
        CoMat = np.delete(CoMat, (0), axis=0)
        CoMat = np.delete(CoMat, (0), axis=1)
        # Normalize
        CoMat = CoMat.astype(np.float64)
        glcm_sums = np.apply_over_axes(np.sum, CoMat, axes=(0, 1))
        glcm_sums[glcm_sums == 0] = 1
        CoMat /= glcm_sums
        
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
    
