import numpy
import scipy.misc


blue = "Blue-Monster.png"
green = "Green-Monster.png"
orange = "Orange-Monster.png"
purple = "Purple-Monster.png"

blueM = scipy.misc.imread(blue,flatten=True)

greenM = scipy.misc.imread(green,flatten=True)

orangeM = scipy.misc.imread(orange,flatten=True)

purpleM = scipy.misc.imread(purple,flatten=True)

### Isotropic Gray-Level Co-Occurance Matrix ###
### Function GLCM takes an arbitrarily sized integer matrix (Img) and neighboorhood size (nhood) and returns the co occurance matrix (CoMat). Entry in CoMat(i,j) is the number of times pixel value i and j co occur within neighboorhood nhood in Img. It is a symmetric matrix. Requires numpy module. ###

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

coBlue = IGLCM(blueM,1)
coGreen = IGLCM(greenM,1)
coOrange = IGLCM(orangeM,1)
coPurple = IGLCM(purpleM,1)


numpy.save("coBlue.tbl",coBlue)
numpy.save("coGreen.tbl",coGreen)
numpy.save("coOrange.tbl",coOrange)
numpy.save("coPurple.tbl",coPurple)







