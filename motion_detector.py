# -*- coding: utf-8 -*-
"""

@author: Priyank Makwana - MIT2020045
"""

#!/usr/bin/env python3

#Import Libraries
import cv2
import numpy as np

#Initializing the camera
cam=cv2.VideoCapture(0)

#Functon to calculate difference of 2 images
def image_diff(image1,image2,image3):
	diff_1_2=cv2.absdiff(image1,image2)
	diff_2_3=cv2.absdiff(image2,image3)
	result_image=cv2.bitwise_and(diff_1_2,diff_2_3)
	return result_image
	

if __name__=='__main__':
    #capturimg the initial frame for initialization
    frame1=cam.read()[1]
    frame2=cam.read()[1]
    frame3=cam.read()[1]

    #converting initial frames into gray-scale
    gray1=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    gray2=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    gray3=cv2.cvtColor(frame3,cv2.COLOR_BGR2GRAY)
    
    #removing the noise and smoothing the image
    gray1=cv2.GaussianBlur(gray1, (21, 21), 0)
    gray2=cv2.GaussianBlur(gray2, (21, 21), 0)
    gray3=cv2.GaussianBlur(gray3, (21, 21), 0)
    
    while 1:
        #Featching the computed image ad processing it
        computed_img=image_diff(gray1,gray2,gray3)
        thresh_converted_img = cv2.threshold(computed_img, 25, 255, cv2.THRESH_BINARY)[1]	#min-25
        #thresh_converted_img = cv2.dilate(thresh_converted_img, None, iterations=1)		#iteration-2
        
        #checking if motion exists
        if np.count_nonzero(thresh_converted_img)>0:
            print("Motion Detected")
        else:
            print("No Motion")
        cv2.imshow('Motion Platform',thresh_converted_img)
        
        #re-calculating the corresponding set of frames
        status,frame=cam.read()
        gray1=gray2
        gray2=gray3
        gray3=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #gray3=cv2.GaussianBlur(gray3, (21, 21), 0)
        
        #exit on user quit input
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break    
        
    #releasing the occupied resources
    cv2.destroyAllWindows()
    cam.release()