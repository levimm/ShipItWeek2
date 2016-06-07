import numpy as np
import cv2

im = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\burst02.JPG')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cv2.imshow('selfImage', imgray)

ret,thresh = cv2.threshold(imgray,100,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


img = cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow('selfImage', img)
cv2.waitKey(0)
cv2.destroyAllWindows()