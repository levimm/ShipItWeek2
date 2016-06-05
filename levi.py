import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('C:\Users\lma5\Pictures\Levi.jpg', cv2.IMREAD_COLOR)

cv2.imshow('selfImage', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# in opencv, images are read in b g r mode. Transfer it to r g b to show in matplot
[b,g,r] = cv2.split(img)
print cv2.split(img)
img2 = cv2.merge([r,g,b])
plt.imshow(img2, interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.show()

