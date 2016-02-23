## PCA Test
import pandas as pd
import numpy as np
from sklearn import decomposition

# Creates index of participant names
participant = list(range(1,17))
for x in range(0,len(participant)):
	participant[x] = "P" +  str(participant[x])

# Creates the initial dataset
price = pd.Series([6,7,6,5,7,6,5,6,3,1,2,5,2,3,1,2],name='price',index=participant)
software = pd.Series([5,3,4,7,7,4,7,5,5,3,6,7,4,5,6,3],name='software',index=participant)
aesthetics = pd.Series([3,2,4,1,5,2,2,4,6,7,6,7,5,6,5,7],name='aesthetics',index=participant)
brand = pd.Series([4,2,5,3,5,3,1,4,7,5,7,6,6,5,5,7],name='brand',index=participant)
data = pd.concat([price,software,aesthetics,brand],axis=1)


# Says that we want 3 output eigenvectors
pca = decomposition.PCA(n_components = 3)

# Saves the eigenvector variance
X = pca.fit(data)
eigenvec = X.explained_variance_ratio_


# Re-adds indices to data, transforms back to pandas dataframe
column_name = list(range(1,len(eigenvec)+1))
for x in range(0,len(column_name)):
	column_name[x] = "PC" + str(column_name[x])
out = pca.transform(data)
pcaOut = pd.DataFrame(data = out, index = participant, columns = column_name)


# Prints data
print(pcaOut)