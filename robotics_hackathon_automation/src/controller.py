#!/usr/bin/env python3
# Remember to change the coordinates recieved by the planner from (X, Y) to (X + 1.79, Y + 0.66).
#you need to name this node "controller"

#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import atan2, sqrt

class TurtleBotController:
    def __init__(self):
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = Odometry().pose.pose
        self.original_target_points = [(-5.06, -3.12), (-5.030810611572746, -2.964564276874691), (-5.006301016800769, -2.772969051635586)]
        self.target_points = [(x + 1.79, y + 0.66) for x, y in self.original_target_points]
        self.current_target = 0

    def odom_callback(self, odom_msg):
        print(odom_msg.pose.pose)
        self.current_pose = odom_msg.pose.pose

    def get_distance_to_target(self, target_point):
        if self.current_pose is None:
            return float('inf')
        dx = self.current_pose.position.x - target_point[0]
        dy = self.current_pose.position.y - target_point[1]
        return sqrt(dx**2 + dy**2)

    def navigate_to_next_point(self):
        target_point = self.target_points[self.current_target]
        while self.get_distance_to_target(target_point) > 0.1:
            dx = target_point[0] - self.current_pose.position.x
            # self.current_pose.position.x
            dy = target_point[1] - self.current_pose.position.y
            desired_angle = atan2(dy, dx)
            
            cmd_vel = Twist()
            cmd_vel.linear.x = 0.1  # adjust the linear velocity
            cmd_vel.angular.z = 0.5 * (desired_angle - self.get_yaw())
            
            self.velocity_publisher.publish(cmd_vel)
            self.rate.sleep()

        self.current_target += 1
        if self.current_target >= len(self.target_points):
            rospy.loginfo("All points reached!")
            rospy.signal_shutdown("All points reached")

    def get_yaw(self):
        return self.current_pose.orientation.z  # You might need to adjust this to get the yaw angle properly

    def run(self):
        while not rospy.is_shutdown() and self.current_target < len(self.target_points):
            self.navigate_to_next_point()

if __name__ == '__main__':
    try:
        controller = TurtleBotController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
