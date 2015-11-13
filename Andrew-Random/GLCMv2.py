def GLCM(Img,nhood):
    CoMatDim=(np.amax(Img)+1,np.amax(Img)+1) #Dimensions of CoMat are 0 to max(Img), +1 because of the way python indexes arrays
    CoMat=np.zeros(CoMatDim,dtype=np.int) #Initialize CoMat as matrix of zeros
    for m in range(-nhood,nhood+1): #loops s.t. only half the displacememnt directions are done, CoMat later transposed and added to itself
        for n in range(0,nhood+1):

            if m<=0 and n==0:
                continue

            ImgCopy1=Img #Copy Img so as not to alter it every loop
            ImgCopy2=Img

            if m>0:
                ImgCopy1RowKeep=np.arange(m,Img.shape[0])
                ImgCopy2RowKeep=np.arange(0,Img.shape[0]-m)
                ImgCopy1=Img[ImgCopy1RowKeep,:]
                ImgCopy2=Img[ImgCopy2RowKeep,:]

            if m<0:
                ImgCopy1RowKeep=np.arange(0,Img.shape[0]+m)
                ImgCopy2RowKeep=np.arange(-m,Img.shape[0])
                ImgCopy1=Img[ImgCopy1RowKeep,:]
                ImgCopy2=Img[ImgCopy2RowKeep,:]

            if n>0:
                ImgCopy1ColKeep=np.arange(n,Img.shape[0])
                ImgCopy2ColKeep=np.arange(0,Img.shape[0]-n)
                ImgCopy1=ImgCopy1[:,ImgCopy1ColKeep]
                ImgCopy2=ImgCopy2[:,ImgCopy2ColKeep]
            
            ImgFlat1=np.ndarray.flatten(ImgCopy1)
            ImgFlat2=np.ndarray.flatten(ImgCopy2)
            
            for d in range(0,ImgFlat1.shape[0]):
                CoMat[ImgFlat1[d],ImgFlat2[d]]=CoMat[ImgFlat1[d],ImgFlat2[d]]+1


    CoMat=CoMat+np.transpose(CoMat)
    return [CoMat]
