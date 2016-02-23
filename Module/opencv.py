ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)






 for i in xrange(6):
   16     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
   17     plt.title(titles[i])
   18     plt.xticks([]),plt.yticks([])
   19 
   20 plt.show()

for i in xrange(6):
	plt.subplot(2,3,i+1),plt.imshow(images[i],"gray")
	plt.title(titles[i])
	plt.xticks([]),plt.yticks([])

plt.show



