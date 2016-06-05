import numpy as np
import cv2

img = cv2.imread('C:\Users\lma5\Pictures\Levi.jpg', cv2.IMREAD_COLOR)

print img[100, 200]

print img.item(100, 200, 2)
print img[100, 200, 2]

img.itemset((100, 200, 1), 0)
print img[100, 200]

print img.shape
print img.size
print img.dtype

somepart = img[50:100, 70:150]
img[0:50, 0:80] = somepart

print img[:,:,0]
img[:,:,2]=0

cv2.imshow('selfImage', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
