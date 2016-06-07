import numpy as np
import cv2
import copy

# some parameters
debug = False
gaussian_parameter = 51 # larger, blurer, better to extract moving object
small_area = 3000 # filter out the small contours that's not people
resize_width = 500
resize_height = 500

# some global variables
first_processing = True
img_list = []
img_copy_list = []
rec_list = []
img_fixed_list = []
img_index = -1
idx2rec = {}

# background subtraction methods
cv2.ocl.setUseOpenCL(False)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 16, False)

# go through the sample images and detect the motion object
for num in range(2968, 2990): # 2968-2984  2920-2929  
	img_name = 'C:\\Users\\lma5\\Pictures\\burst\\IMG_' + str(num) + '.JPG'
	img = cv2.imread(img_name, cv2.IMREAD_COLOR)
	if img is not None:

		# scale first to 500*500
		img = cv2.resize(img, (resize_width, resize_height), interpolation = cv2.INTER_CUBIC)

		img_index += 1
		idx2rec[img_index] = []

		# change to grayscale for better result
		gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gimg = cv2.GaussianBlur(gimg, (gaussian_parameter, gaussian_parameter), 0) # larger the parameter, blurer
		# extract the moving object
		fgmask = fgbg.apply(gimg)
		# denoise
		dst = cv2.fastNlMeansDenoising(fgmask,None,300,9,23)
		# find the contours
		img_find_contour, contours, hierarchy = cv2.findContours(dst,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# draw the bounding rectangle
		for cnt in contours:
			if cv2.contourArea(cnt) < small_area:
				continue

			# drawing contours of moving people, use rectangle to fit in this application
			if debug:
				img_draw_contour = cv2.drawContours(img, [cnt], 0, (0,255,0), 2)
				cv2.imshow('frame',img_draw_contour)
				key = cv2.waitKey(0) 

			# bound to rectangle
			x,y,w,h = cv2.boundingRect(cnt)
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),-1)
			idx2rec[img_index].append((x, y, w, h))


		# add to global list
		img_list.append(img)

if debug:
	for img in img_list:
		cv2.imshow('frame',img)
		key = cv2.waitKey(0) 

# make a deep copy of all processed images
img_copy_list = copy.deepcopy(img_list)

# function to determine if two rectangle intersects with each other
def intersect(roi1, roi2):
	x1, y1, w1, h1 = roi1
	x2, y2, w2, h2 = roi2
	if x1+w1 < x2:
		return False
	elif y1+h1 < y2:
		return False
	elif x1 > x2+w2:
		return False
	elif y1 > y2+h2:
		return False
	else:
		return True

# go through the processed images and find the replace region
for i, img in enumerate(img_list):

	### directly copy region
	if i == 0: continue  # skip first image cause it is bot recgonizable

	# find the x, y, w, h for i
	for base_region in idx2rec[i]:
		print "{} img".format(i)
		print base_region

		replace_roi_1 = None
		replace_roi_2 = None
		replace_roi = None # the real region to replace
		j = i + 1
		k = i - 1

		# search forward
		while j <= img_index:
			# in the j th image
			print "{} img".format(j)
			replaceable = True
			for rec_region in idx2rec[j]:
				if intersect(base_region, rec_region):
					print "intersect"
					replaceable = False
					break
			if replaceable:
				print "replaceable"
				x, y, w, h = base_region
				# (img_list[i])[y:y+h, x:x+w] = (img_copy_list[j])[y:y+h, x:x+w]
				# the +1, -1 is used for the following inpaint
				replace_roi_1 = (img_copy_list[j])[y+1:y+h-1, x+1:x+w-1]
				# cv2.imshow('frame',tmproi)
				# key = cv2.waitKey(0)
				break
			else:
				j += 1

		# search backword
		while k >= 1:
			replaceable = True
			for rec_region in idx2rec[k]:
				if intersect(base_region, rec_region):
					print "intersect"
					replaceable = False
					break
			if replaceable:
				print "replaceable"
				x, y, w, h = base_region
				# the +1, -1 is used for the following inpaint
				replace_roi_2 = (img_copy_list[k])[y+1:y+h-1, x+1:x+w-1]
				# cv2.imshow('frame',tmproi)
				# key = cv2.waitKey(0)
				break
			else:
				k -= 1

		# blend the two consucutive regions
		if replace_roi_1 is not None:
			replace_roi = replace_roi_1
		if replace_roi_2 is not None:
			if replace_roi is not None:
				replace_roi = cv2.addWeighted(replace_roi, 0.8, replace_roi_2, 0.2, 0)
			else:
				replace_roi = replace_roi_2

		(img_list[i])[y+1:y+h-1, x+1:x+w-1] = replace_roi
		# cv2.imshow('frame',replace_roi)
		# key = cv2.waitKey(0) 


	# use bitwise operations(or, xor), not good enough
	# if index == 0:
	# 	img_result = img
	# img_result = cv2.bitwise_xor(img_result, img)

# inpaint for the boundary
for i, img in enumerate(img_list):
	if i == 0: continue
	mask = np.zeros((resize_width, resize_height, 1), np.uint8)
	for base_region in idx2rec[i]:
		x, y, w, h = base_region
		mask = cv2.rectangle(mask, (x, y), (x+w, y+h), (255, 255, 255), 2)
	img_fixed = cv2.inpaint(img, mask, 2, cv2.INPAINT_TELEA)
	img_fixed_list.append(img_fixed)
	if debug:
		cv2.imshow('frame',img)
		key = cv2.waitKey(0) 
		cv2.imshow('frame',mask)
		key = cv2.waitKey(0) 
		cv2.imshow('frame',img_fixed)
		key = cv2.waitKey(0) 

for img in img_fixed_list:
	cv2.imshow('frame',img)
	key = cv2.waitKey(0) 
	if key == 27:
		break

cv2.destroyAllWindows()