#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

def image_callback(msg):
    try:
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # Define the blue color range in RGB
        lower_blue = np.array([0, 0, 100])
        upper_blue = np.array([80, 80, 255])
        
        # Define the red color range in RGB
        lower_red = np.array([100, 0, 0])
        upper_red = np.array([255, 80, 80])
        
        # Create masks for blue and red color ranges
        blue_mask = cv2.inRange(cv_image, lower_blue, upper_blue)
        red_mask = cv2.inRange(cv_image, lower_red, upper_red)
        
        # Apply masks to the original image
        blue_result = cv2.bitwise_and(cv_image, cv_image, mask=blue_mask)
        red_result = cv2.bitwise_and(cv_image, cv_image, mask=red_mask)
        
        # Combine the blue and red results
        final_result = cv2.add(blue_result, red_result)
        
        # Display the processed image
        cv2.imshow("Processed Image", final_result)
        cv2.waitKey(1)
    except Exception as e:
        print(e)

def main():
    rospy.init_node("cone_detection_node")
    
    # Subscribe to the camera topic
    rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
    
    # Initialize OpenCV window
    cv2.namedWindow("Processed Image", cv2.WINDOW_NORMAL)
    
    # Keep the script running
    rospy.spin()
    
    # Clean up
    cv2.destroyAllWindows()


main()
