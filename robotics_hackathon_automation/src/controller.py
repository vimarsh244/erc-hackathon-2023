import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2


x = -5.06+1.79
y = -3.12+0.66
theta = 0.0


# List of points to visit
points = [(-5.030810611572746, -2.964564276874691), (-5.006301016800769, -2.772969051635586), 
          (-5.01335232539674, -2.5869961083894406), (-5.0450424106615355, -2.4742728427314002), 
          (-5.036214963592425, -2.383971146520099), (-5.048374125472307, -2.034011051710709)]


points = [(round(x+1.79, 2), round(y+0.66, 2)) for x, y in points]


def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()

r = rospy.Rate(4)

goal = Point()
goal.x = -5.0308+1.79
goal.y = -2.96+0.66

while not rospy.is_shutdown():
    for _x, _y in points:
        
        inc_x = _x -x
        inc_y = _y -y

        angle_to_goal = atan2(inc_y, inc_x)

        if abs(angle_to_goal - theta) > 0.1:
            speed.linear.x = 0.0
            speed.angular.z = 0.3
        else:
            speed.linear.x = 0.5
            speed.angular.z = 0.0

        pub.publish(speed)
        r.sleep()    

