import numpy as np 
import cv2

# create a black image
img = np.zeros((512, 512, 3), np.uint8)

# draw line
img = cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)

# draw rectangle
img = cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)

# draw circle
img = cv2.circle(img, (447, 63), 63, (0, 0, 255), -1) # -1 mean fill the circle

# skip ecllipse and polygon and text

cv2.imshow("test", img)
cv2.waitKey(0)
# Make conflict
cv2.destroyAllWindows()
