import cv2
import numpy as np
import streamlit as st


# Refer to the application notebook implement the following filters
@st.cache_data
def bw_filter(img):
    # Write your code here to convert img to a gray image
	img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
	return img_gray

@st.cache_data
def vignette(img, level):
	if level == 0:
		return img
	else:
		height, width = img.shape[:2]  

		# Generate vignette mask using Gaussian kernels.
		X_resultant_kernel = cv2.getGaussianKernel(width, width/level)
		Y_resultant_kernel = cv2.getGaussianKernel(height, height/level)
			
		# Generating resultant_kernel matrix.
		# H x 1 * 1 x W
		kernel = Y_resultant_kernel * X_resultant_kernel.T 
		mask = kernel / kernel.max()
		
		img_vignette = np.copy(img)
			
		# Applying the mask to each channel in the input image.
		for i in range(3):
			img_vignette[:,:,i] = img_vignette[:,:,i] * mask

		return img_vignette

@st.cache_data
def sepia(img):
	 # Write your code here to create the sepia effect
	img_sepia = img.copy()
    # Converting to RGB as sepia matrix below is for RGB.
	img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB) 
	img_sepia = np.array(img_sepia, dtype = np.float64)
	img_sepia = cv2.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                    [0.349, 0.686, 0.168],
                                                    [0.272, 0.534, 0.131]]))
    # Clip values to the range [0, 255].
	img_sepia = np.clip(img_sepia, 0, 255)
	img_sepia = np.array(img_sepia, dtype = np.uint8)
	img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)
	return img_sepia

@st.cache_data
def pencil_sketch(img, ksize=5):
	 # Write your code here to create the pencil sketch effect
	img_blur = cv2.GaussianBlur(img, (5,5), 0, 0)
	img_sketch, _ = cv2.pencilSketch(img_blur)
	return img_sketch

# Don't be constrained, add your own filters here

@st.cache_data
def bright(img, level):
    img_bright = cv2.convertScaleAbs(img, beta = level)
    return img_bright

@st.cache_data
def contrast(img, level):
    img_contrast = cv2.convertScaleAbs(img, alpha = level)
    return img_contrast

