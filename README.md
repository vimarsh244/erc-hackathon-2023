# NEW

### Mechanical

**Design**:

![3D model render](/mechanical/3d_model.png)

Model files can be found in the mechanical/ directory. https://a360.co/45wuxL5

**Ansys Analysis**:



### Electronics

Part 1:

https://www.tinkercad.com/things/8tS4cQEKOlx?sharecode=zMyGMb17AG04Dq2QzwaMsAUVSxyepGBn6ncqBjoWyT0

The differential drive mechanism is a simple 4wd that takes in (linear.x and angular.z) from ROS controller which will accordingly turn the motors.


Part 2:

https://www.tinkercad.com/things/5scrJineZXJ?sharecode=lACrRppUO8Gc_l1i7u2KO_VQ8Vd_mAQmPxYdKY659Rk


Part 3-6:

https://www.tinkercad.com/things/doNj9fPPetp?sharecode=6bNxCSpgDcdtsFkDNGaQSvCr4-Utx1kQABxrum8ldWc

Combined all tasks in one circuit


#### Coil Mechanism

The Sinosoidal wave produced will be connected to a copper coil. Another copper coil will be receiving the voltage. When connected across a capcitor and near a mine, due to metal eddy currents, there will be changes across voltage in capacitor measured by any ADC converter.


### Automation

**Colour Detection**




**Path Planning**

![Path Planning Algorithm](misc/latest_6_robot_auto_navigates_with_publish_subscribe.png)


**Others**

run `catkin_make` after cloning in the `~/catkin_ws/src` disctory.

Path planner uses RRT to make calculate a path which goes over all points.

Due to time constraints I could not make a good PID controller, just made a simple controller to go from one point to another.

