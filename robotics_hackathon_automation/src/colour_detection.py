#!/usr/bin/env python3
#You need to name this node "color_detector"
#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

def image_callback(msg):
    try:
        # Convert ROS image to OpenCV image
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv2.imshow("Processed Image", cv_image)
        # Define the blue color range in HSV
        # Define the blue color range in RGB
        lower_blue = np.array([10, 20, 0])
        upper_blue = np.array([50, 90, 255])
        
        # Define the red color range in RGB
        lower_red = np.array([60, 0, 0])
        upper_red = np.array([255, 50, 50])
        
        # Create masks for blue and red color ranges
        blue_mask = cv2.inRange(rgb_image, lower_blue, upper_blue)
        red_mask = cv2.inRange(rgb_image, lower_red, upper_red)
        
        blue_px_detected = np.sum(blue_mask)
        red_px_detected = np.sum(red_mask)

        if(blue_px_detected>0):
            print("Iron extraction ongoing")
        if(red_px_detected>0):
            print("Zinc extraction ongoing")
        # Apply masks to the original image
        blue_result = cv2.bitwise_and(cv_image, cv_image, mask=blue_mask)
        red_result = cv2.bitwise_and(cv_image, cv_image, mask=red_mask)
        cv2.imshow("red color detection", red_result) 
        cv2.imshow("blue color detection", blue_result)
        cv2.waitKey(0) 

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

# if _name_ == "_main_":
main()