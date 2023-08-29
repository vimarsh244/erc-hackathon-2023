import rospy
from std_msgs.msg import String
from time import sleep
rospy.init_node('path_planner', anonymous=True)
# path_pub = rospy.Publisher('/planned_path', PointArray, queue_size=10)  # Replace 'point_array_topic' with your desired topic name

array_pub = rospy.Publisher('/planned_path', String, queue_size=10)  # Replace 'point_array_topic' with your desired topic name

with open("paths_data_temp.txt", "r") as f:
    
    array_string = f.read()

hello_str = "hello world %s" % rospy.get_time()

print(array_string)
# Publish the array string as a ROS message

rate = rospy.Rate(10)

# while not rospy.is_shutdown():
#     array_pub.publish(array_string)
    # rate.sleep()

sleep(5)

array_pub.publish(array_string)

# rospy.spin()



