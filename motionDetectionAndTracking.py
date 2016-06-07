import numpy as np
import cv2

img_pre = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\IMG_2968.JPG', cv2.IMREAD_COLOR)
gimg_pre = cv2.cvtColor(img_pre, cv2.COLOR_BGR2GRAY)
gimg_pre = cv2.GaussianBlur(gimg_pre, (21, 21), 0)
for num in range(2969, 2983): #2969-2984  2920-2929
	img_name = 'C:\\Users\\lma5\\Pictures\\burst\\IMG_' + str(num) + '.JPG'
	img = cv2.imread(img_name, cv2.IMREAD_COLOR)
	if img is not None:
		gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gimg = cv2.GaussianBlur(gimg, (21, 21), 0)
		imgDelta = cv2.absdiff(gimg_pre, gimg)
		thresh = cv2.threshold(imgDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts:
			if cv2.contourArea(c) < 100:
				continue
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(gimg, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#cv2.imshow('frame',dst)
		k = cv2.waitKey(0) 
		if k == 27:
			break

cv2.destroyAllWindows()