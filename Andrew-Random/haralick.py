import numpy as np
import math as mt

### Still untested!
### Reference document: http://www.uio.no/studier/emner/matnat/ifi/INF4300/h08/undervisningsmateriale/glcm.pdf
### This script has the different functions that are defined to extract Haralick features from an IGLCM
# Why isn't this working?

## Angular Second Moment(ASM) / Energy is a measure of homogeneity in an image
def ASM(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += (CoMat[i][j])**2
	return val

## Contrast adds the comatrival, but favours when values are away from the diagonal
def Contrast(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += (CoMat[i][j]) * (abs(i-j)**2)
	return val

## Local homogeneity (Inverse Difference Moment)
def IDM(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += (CoMat[i][j]) * 1/(1+(i-j)**2)
	return val
	
## Entropy
def entropy(CoMat):
	val=0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += (CoMat[i][j]) * mt.log(CoMat[i][j])
	return val

## Horizontal Mean
def xmean(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += i * CoMat[i][j]
	return val

## Vertical Mean
def ymean(CoMat):
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += j * CoMat[i][j]
	return val

## Horizontal Standard Deviation
def xstdev(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += ((i-xmean(CoMat))**2) * CoMat[i][j]
	return val

# Vertical Standard Deviation	
def ystdev(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += ((j-xmean(CoMat))**2) * CoMat[i][j]
	return val

## The actual correlation function, requires the above calculations
def CORR(CoMat):
	val = 0
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += ((i*j) * CoMat[i][j] - (xmean(CoMat)-ymean(CoMat)))/(xstdev(CoMat)*ystdev(CoMat))
	return val

# Total Mean
def mean(CoMat):
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += CoMat[i][j]
	num = CoMat.shape[0] * CoMat.shape[1]
	mean = val / num
	return mean

# Sum of Squares, Variance
def variance(CoMat):
	for i in range(0,CoMat.shape[0]-1)
		for j in range(0,CoMat.shape[1]-1)
			val += (i-mean(CoMat))**2 * CoMat[i][j]
	return val

# Sum Average





















