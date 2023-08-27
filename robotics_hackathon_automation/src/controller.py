import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2


x = -5.06+1.79
y = -3.12+0.66
theta = 0.0


# List of points to visit
points = [(-5.030810611572746, -2.964564276874691), (-5.006301016800769, -2.772969051635586), (-5.01335232539674, -2.5869961083894406), (-5.0450424106615355, -2.4742728427314002), (-5.036214963592425, -2.383971146520099), (-5.048374125472307, -2.034011051710709), (-5.00086422271461, -1.6450587512478214), (-4.953175960331631, -1.436101148115933), (-4.077540661420645, -1.5098627014586885), (-3.964773531420417, -1.2972558822352236), (-3.8118017351888445, -1.3840735612624258), (-3.730303603001504, -1.3985485675835183), (-3.7094535144307286, -1.443201587020344), (-3.66014838330777, -1.4819410170281346), (-3.659422999851919, -1.4884405543523012), (-3.645538366097871, -1.5208430744444097), (-3.649380984679647, -1.5338828589666225), (-3.648125332166168, -1.5780470550398351), (-3.647528984405044, -1.5781526943731792), (-3.648074238280723, -1.5985197576104515), (-3.641469765787517, -1.6613114327598377), (-3.6493182973227603, -1.7084494314381997), (-3.6492284831870823, -1.7331566628068178), (-3.6623673716900242, -1.7343471675100866), (-3.6670099619860563, -1.7740512044370738), (-3.637716655143843, -1.815783523506243), (-3.642944706144448, -1.8634714350453014), (-3.6505573239646565, -1.8982610434254046), (-3.6465919033648135, -1.9169042789395478), (-3.653529349540879, -1.95484288696686), (-3.660604510363207, -1.9591801976824197), (-3.6763174822439173, -1.9608366327179696), (-3.684633560624374, -1.9644091171813383), (-3.6955341450816475, -1.9935269194503724), (-3.7024072189383572, -2.017530873690399), (-3.6954383385730445, -2.036931356671339), (-3.61, -2.2)]


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
# goal.x = -5.0308+1.79
# goal.y = -2.96+0.66

i = 0
goal.x = points[i][0]
goal.y = points[i][1]
print(goal)


while not rospy.is_shutdown():
    inc_x = goal.x -x
    inc_y = goal.y -y

    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.2
    else:
        speed.linear.x = 0.1
        speed.angular.z = 0.0

    if(inc_x < 0.1 and inc_y < 0.1 and (angle_to_goal-theta) < 0.1):
        i= i+1
        goal.x = points[i][0]
        goal.y = points[i][1]
        print(goal)
        

    pub.publish(speed)
    r.sleep()

