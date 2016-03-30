import numpy as np
import math as mt

### Still untested!
### Reference document: http://www.uio.no/studier/emner/matnat/ifi/INF4300/h08/undervisningsmateriale/glcm.pdf
### This script has the different functions that are defined to extract Haralick features from an IGLCM


def haralickALL(CoMat):
	np.array([
		ASM(CoMat),
		contrast(CoMat),
		IDM(CoMat),
		entropy(CoMat),
		xmean(CoMat),
		ymean(CoMat),
		xstdev(CoMat),
		ystdev(CoMat),
		CORR(CoMat),
		mean(CoMat),
		variance(CoMat),
		xPlusY(CoMat),
		sumAverage(CoMat),
		sumEntropy(CoMat),
		difEntropy(CoMat),
		inertia(CoMat),
		clusterShade(CoMat),
		clusterProm(CoMat),
	])


	




## Angular Second Moment(ASM) / Energy is a measure of homogeneity in an image
def ASM(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (CoMat[i][j])**2
	return val

	


## Contrast adds the comatrival, but favours when values are away from the diagonal
def contrast(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (CoMat[i][j]) * (abs(i-j)**2)
	return val

## Local homogeneity (Inverse Difference Moment)
def IDM(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (CoMat[i][j]) * 1/(1+(i-j)**2)
	return val
	
## Entropy (Log function had to have a +1 to ensure that values are not zero)
def entropy(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (CoMat[i][j]) * mt.log(CoMat[i][j]+1)
	return val * (-1)

## Horizontal Mean
def xmean(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += i * CoMat[i][j]
	return val

## Vertical Mean
def ymean(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += j * CoMat[i][j]
	return val

## Horizontal Standard Deviation
def xstdev(CoMat):
	val = 0
	xmeanVal = xmean(CoMat)
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += ((i-xmeanVal)**2) * CoMat[i][j]
	return val	
	
	
	
	
	
	
# Vertical Standard Deviation	
def ystdev(CoMat):
	val = 0
	ymeanVal = ymean(CoMat)
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += ((j-ymeanVal)**2) * CoMat[i][j]
	return val

## The actual correlation function, requires the above calculations
def CORR(CoMat):
	val = 0
	xmeanVal = xmean(CoMat)
	ymeanVal = ymean(CoMat)
	
	xStdVal = xstdev(CoMat)
	yStdVal = ystdev(CoMat)
	
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += ((i*j) * CoMat[i][j] - (xmeanVal-ymeanVal))/(xStdVal*yStdVal)
	return val	

# Total Mean
def mean(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += CoMat[i][j]
	num = CoMat.shape[0] * CoMat.shape[1]
	mean = val / num
	return mean

# Sum of Squares, Variance
def variance(CoMat):
	val = 0
	meanVal = mean(CoMat)
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (i-meanVal)**2 * CoMat[i][j]
	return val



# P(x+y) is the diagonal sum of the matrix.
def xPlusY(CoMat,kValue):
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
def sumAverage(CoMat):
	val = 0
	for k in range(0,CoMat.shape[0]*2-2):
		val += xPlusY(CoMat,k) * k
	return val

# Sum Entropy (Log function had to have a +1 to ensure that values are not zero)
def sumEntropy(CoMat):
	val = 0
	for k in range(0,CoMat.shape[0]*2-2):
		val += xPlusY(CoMat,k)* mt.log(xPlusY(CoMat,k)+1)
	return val*(-1)
	

	
# Differencce Entropy (Log function had to have a +1 to ensure that values are not zero)
def difEntropy(CoMat):
	val = 0
	for k in range(0,CoMat.shape[0]-1):
		val += xPlusY(CoMat,k)* mt.log(xPlusY(CoMat,k)+1)
	return val*(-1)


# Inertia
def inertia(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += ((i-j)**2) * CoMat[i][j]
	return val
	
	
# Cluster Shade
def clusterShade(CoMat):
	val = 0
	ux = xmean(CoMat)
	uy = ymean(CoMat)
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (i + j - ux - uy)**3 * CoMat[i][j]
	return val
	

# Cluster Prominance
def clusterProm(CoMat):
	val = 0
	ux = xmean(CoMat)
	uy = ymean(CoMat)
	for i in range(0,CoMat.shape[0]-1):
		for j in range(0,CoMat.shape[1]-1):
			val += (i + j - ux - uy)**4 * CoMat[i][j]
	return val












