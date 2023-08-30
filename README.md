# ERC Hackathon 2023 submission

### Mechanical

**Design**:

![3D model render](/mechanical/3d_model.png)

Model files can be found in the `mechanical/` directory or https://a360.co/45wuxL5

**Ansys Analysis**:

Report can be found [here](mechanical/ansys%20analysis/ERC%20HACK%20ANSYS%20MINED.pdf)

### Electronics

![PCB Design Sample](electronics/PCB%203-7.png)

Part 1:

[link](https://www.tinkercad.com/things/8tS4cQEKOlx?sharecode=zMyGMb17AG04Dq2QzwaMsAUVSxyepGBn6ncqBjoWyT0)

The differential drive mechanism is a simple 4wd that takes in (linear.x and angular.z) from ROS controller which will accordingly turn the motors.


Part 2:

[link](https://www.tinkercad.com/things/2AzpW1k3oru?sharecode=b2Rh3jejDMBBp6OE0veHATIasINy7RtwA5-mOQYV0L8)


Part 3-6:

[link](https://www.tinkercad.com/things/doNj9fPPetp?sharecode=6bNxCSpgDcdtsFkDNGaQSvCr4-Utx1kQABxrum8ldWc)

Combined all tasks in one circuit.


#### Coil Mechanism

The Sinusoidal wave produced will be connected to a copper coil (basically an inductor). Another copper coil will be receiving the voltage. When connected across a capacitor and near a mine, due to metal eddy currents, there will be changes across voltage in capacitor measured by Arduino.


#### PCBs

The necessary PCBs can be fouond in the `electronics/` directory.

### Automation

**Color Detection**

Cone detection as follows:
![Cone Detection](misc/blue_cone_detect.png)

**Path Planning**

![Path Planning Algorithm](misc/latest_6_robot_auto_navigates_with_publish_subscribe.png)


**Others**

run `catkin_make` after cloning in the `~/catkin_ws/src` directory.

Path planner uses RRT to make calculate a path which goes over all points.
