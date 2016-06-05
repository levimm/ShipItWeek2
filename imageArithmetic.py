import numpy as np
import cv2

x = np.uint8([250])

# print cv2.add(x, x)

img1 = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\burst01.JPG', cv2.IMREAD_COLOR)
img2 = cv2.imread('C:\\Users\\lma5\\Pictures\\burst\\burst02.JPG', cv2.IMREAD_COLOR)
# img = cv2.resize(img,  (100,100))

result_opencv = cv2.add(img1, img2) # saturation 
result_numpy = img1 + img2 # modulo

# image blending
result_blend = cv2.addWeighted(img1, 0.8, img2, 0.2, 0)

# bitwise operation
rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
dst = cv2.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst

cv2.imshow('selfImage', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()