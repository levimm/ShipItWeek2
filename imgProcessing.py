import cv2

img1 = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\burst01.JPG', cv2.IMREAD_COLOR)
img2 = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\burst02.JPG', cv2.IMREAD_COLOR)

blur1 = cv2.blur(img1, (3, 3))
blur2 = cv2.blur(img2, (3, 3))
tmp1 = cv2.bitwise_and(img1,img2)
tmp2 = cv2.bitwise_and(blur1,blur2)

gaussian_blur = cv2.GaussianBlur(img2,(3,3),0)
median = cv2.medianBlur(img2,5)
bilateral_blur = cv2.bilateralFilter(img2,9,75,75)

tmp = cv2.bitwise_and(img1,img2)

gimg = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
print gimg.shape
cimg = cv2.cvtColor(gimg, cv2.COLOR_GRAY2BGR)
print cimg.shape

cv2.imshow('selfImage', tmp2)
cv2.waitKey(0)
cv2.destroyAllWindows()
