import time
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from robotics_hackathon_automation.msg import PointArray 
from math import atan2, sqrt
import std_msgs

import re ##regex use :((


class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value):
        """Calculates PID value for given reference feedback"""
        error = self.SetPoint - feedback_value

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

x = 0.0
y = 0.0
theta = 0.0
points = []



# [
#     [(x,y),(p,q),...],[(x,y),(p,q),...],[(x,y),(p,q),...],[(x,y),(p,q),...],
# ]


def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("tb3_controller")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()


def convert_and_modify_path(custom_schema_path):
    modified_path = []
    for point in custom_schema_path:
        modified_x = point.x + 1.79  # Adding X offset
        modified_y = point.y + 0.66  # Adding Y offset
        modified_path.append(Point(x=modified_x, y=modified_y))
    print(modified_path)
    return modified_path

def subscriber_callback(data):
    # Convert the modified array string back to a list of paths
    string_ = data.data
    print(string_[0])
    print(type(string_))
    modified_paths = eval(data.data)

    print(modified_path)
    for path in modified_paths:
        modified_path = convert_and_modify_path(path)
        print("Modified Path:")
        for point in modified_path:
            print(f"X: {point.x}, Y: {point.y}")


rospy.Subscriber('/planned_path', std_msgs.msg.String, subscriber_callback)



# Subscribe to the array string topic
# rospy.Subscriber("/planned_path", std_msgs.msg.String, array_string_callback)

r = rospy.Rate(50)
pid = PID()

while not rospy.is_shutdown():
    if points:
        goal = Point()
        goal.x = points[0][0]
        goal.y = points[0][1]   

        inc_x = goal.x - x
        inc_y = goal.y - y

        angle_to_goal = atan2(inc_y, inc_x)

        pid.SetPoint = angle_to_goal
        pid.update(theta)

        speed.angular.z = pid.output
        speed.linear.x = 0.2

        # If we're close to the goal
        if sqrt(inc_x**2 + inc_y**2) < 0.5:
            speed.linear.x = 0
            points.pop(0) # Delete the point from the list
        
        pub.publish(speed)

    r.sleep()