import timing
import numpy as np
import math as mt

# Imports all the functions
import haralick as hck





# Arbitrary cooccurance matrix
coMat = np.load("screen.npy")


# Testing all of the functions.. they work!
print("ASM is: ",hck.ASM(coMat),"\n")
print("Contrast is: ",hck.contrast(coMat),"\n")
print("Local homogeneity is: ",hck.IDM(coMat),"\n")
print("Entropy is: ",hck.entropy(coMat),"\n")
print("X-Mean is: ",hck.xmean(coMat),"\n")
print("Y-Mean is: ",hck.ymean(coMat),"\n")
print("X-Standard Deviation is: ",hck.xstdev(coMat),"\n")
print("Y-Standard Deviation is: ",hck.xstdev(coMat),"\n")
print("Correlation is: ",hck.CORR(coMat),"\n")
print("Mean is: ",hck.mean(coMat),"\n")
print("Variance is: ",hck.variance(coMat),"\n")
print("X plus Y for k-value 170 is: ", hck.xPlusY(coMat,166),"\n")
print("Sum Average is: ",hck.sumAverage(coMat),"\n")
print("Sum Etropy is: ",hck.sumEntropy(coMat),"\n")
print("Difference Entropy is: ",hck.difEntropy(coMat),"\n")
print("Inertia is: ",hck.inertia(coMat),"\n")
print("Cluster Shade is: ",hck.clusterShade(coMat),"\n")
print("Cluster Prominence is: ",hck.clusterProm(coMat),"\n")




