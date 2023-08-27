#!/usr/bin/env python


# https://github.com/kulbir-ahluwalia/Turtlebot_3_PID/blob/master/control_bot/Scripts/final.py
# seems quite good pid

import rospy
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations
import math

class TurtlebotController:

    def __init__(self):
        # setup ROS node
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.callback)
        self.pose = {'x': -5.06+1.79, 'y': -3.12+0.66, 'theta': 0.0}

        # (-5.06, -3.12)
        # define turtlebot speed boundaries
        self.speed = Twist()
        self.speed.linear.x = 0.2  # maximum linear velocity
        self.speed.angular.z = 1.5  # maximum angular velocity

        self.points = [(-5.030810611572746, -2.964564276874691), 
                       (-5.006301016800769, -2.772969051635586), (-5.01335232539674, -2.5869961083894406), 
                       (-5.0450424106615355, -2.4742728427314002), 
                       (-5.036214963592425, -2.383971146520099), 
                       (-5.048374125472307, -2.034011051710709)]
        
        self.points = [(x+1.79, y+0.66) for x, y in self.points]


#

        self.goal = Point()
        self.get_goal()

    def callback(self, data):
        # callback method for the subscriber
        self.pose['x'] = data.pose.pose.position.x
        self.pose['y'] = data.pose.pose.position.y
        rot_q = data.pose.pose.orientation
        _, _, self.pose['theta'] = transformations.euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

    def get_goal(self):
        # update goal point
        self.goal.x = self.points[0][0]
        self.goal.y = self.points[0][1]
        self.points.pop(0)

    def move2goal(self):
        # move turtlebot to the goal
        goal_reached = False

        while goal_reached is False:
            deltaX = self.goal.x - self.pose['x']
            deltaY = self.goal.y - self.pose['y']
            angle_to_goal = math.atan2(deltaY, deltaX)

            if abs(angle_to_goal - self.pose['theta']) > 0.1:
                self.speed.linear.x = 0.0
                self.speed.angular.z = self.speed.angular.z
            else:
                self.speed.linear.x = self.speed.linear.x
                self.speed.angular.z = 0.0

                if abs(deltaX) < 0.1 and abs(deltaY) < 0.1:
                    goal_reached = True
                    self.speed.linear.x = 0.0
                    if len(self.points) > 0:
                        self.get_goal()
                        goal_reached = False

            self.cmd_pub.publish(self.speed)
            rospy.Rate(10).sleep()

if __name__ == "__main__":
    controller = TurtlebotController()
    controller.move2goal()

# List of points to visit
