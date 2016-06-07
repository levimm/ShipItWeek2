import numpy as np 
import cv2

body_cascade = cv2.CascadeClassifier('C:\\Users\\lma5\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('C:\\Users\\lma5\\Downloads\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml')

for num in range(2972, 2990): # 2968-2984  2920-2929  
	img_name = 'C:\\Users\\lma5\\Pictures\\burst\\IMG_' + str(num) + '.JPG'
	img = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\full-body.jpg')
	if img is not None:
		gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		bodies = body_cascade.detectMultiScale(gimg, 1.01, 50)
		faces = face_cascade.detectMultiScale(gimg, 1.1, 5)
		print bodies
		print faces
		for (x, y, w, h) in bodies:
			img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
		cv2.imshow('img',img)
		key = cv2.waitKey(0)
		if key == 27:
			break
cv2.destroyAllWindows()