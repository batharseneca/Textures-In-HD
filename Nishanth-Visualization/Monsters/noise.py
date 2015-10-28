import numpy
import scipy.misc



noise = scipy.misc.imread("Capture.PNG",flatten=True)


def IGLCM(Img,nhood):
	CoMatDim=(numpy.amax(Img)+1,numpy.amax(Img)+1) #Dimensions of CoMat are 0 to max(Img), +1 because of the way python indexes arrays#
	CoMat=numpy.zeros(CoMatDim,dtype=numpy.int) #Initialize CoMat as matrix of zeros#
	for i in range(Img.shape[0]): #i is row index of Img#
		for j in range(Img.shape[1]): #j is column index of Img#
			for m in range(-nhood,nhood+1): #m is row displacement from pixel ij#
				for n in range(-nhood,nhood+1): #n is column displacement from pixel ij#
					if i+m>Img.shape[0]-1 or j+n>Img.shape[1]-1 or i+m<0 or j+n<0 or m==0 or n==0: #check whether you are beyond Img border on on current pixel#
						continue
					CoMat[Img[i,j],Img[i+m,j+n]]=CoMat[Img[i,j],Img[i+m,j+n]]+1 #add 1 to position in CoMat where pixels co occur#
	CoMat=numpy.divide(CoMat,numpy.sum(CoMat)) #Normalize CoMat#
	return CoMat
	
coNoise = IGLCM(noise,5)


numpy.save("screen",coNoise)