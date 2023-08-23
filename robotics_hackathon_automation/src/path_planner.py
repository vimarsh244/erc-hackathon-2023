#!/usr/bin/env python3
#Following is the import line for importing the obstacle detection methods i.e. isValidPoint()
#you need to name this node as "path_planner"

# import obstacle_detection as obsdet


import rospy
import random
import math
from obstacle_detection import isValidPoint
from geometry_msgs.msg import Point

import matplotlib.pyplot as plt


class RRTStarPathPlanner:
    def __init__(self):
        rospy.init_node("path_planner")
        
        # Define parameters
        self.start_point = (-5.06, -3.12)
        self.goal_points = [(5.18, -2.19), (1.58, -2.26), (-2.28, 1.86), (0.57, 0.33), (-3.61, -2.20)]
        self.goal_reached_threshold = 0.5
        self.step_size = 0.5
        
        # Initialize RRT data structures
        self.nodes = [self.start_point]
        self.parent = {self.start_point: None}
        
        # Create a ROS publisher for the planned path
        self.path_pub = rospy.Publisher("/planned_path", Point, queue_size=10)
        
    def sample_random_point(self):
        # Sample a random point within a predefined space
        x = random.uniform(-5.0, 5.0)
        y = random.uniform(-3.0, 3.0)
        return x, y
    
    def find_nearest_node(self, point):
        # Find the nearest node in the tree to the sampled point
        nearest_node = min(self.nodes, key=lambda n: math.sqrt((n[0] - point[0])**2 + (n[1] - point[1])**2))
        return nearest_node
    
    def steer_towards_point(self, from_node, to_point):
        # Steer from the nearest node towards the sampled point with a step size
        angle = math.atan2(to_point[1] - from_node[1], to_point[0] - from_node[0])
        new_node = (from_node[0] + self.step_size * math.cos(angle), from_node[1] + self.step_size * math.sin(angle))
        return new_node
    
    def is_obstacle_free(self, from_node, to_node):
        # Check if the path between two nodes is obstacle-free
        return isValidPoint(from_node[0], from_node[1], to_node[0], to_node[1])
    
    def rrt_star_planner(self):
        while not rospy.is_shutdown():
            random_point = self.sample_random_point()
            nearest_node = self.find_nearest_node(random_point)
            new_node = self.steer_towards_point(nearest_node, random_point)
            
            if self.is_obstacle_free(nearest_node, new_node):
                # Find nodes in a radius and update parent if new path is shorter
                near_nodes = [node for node in self.nodes if math.sqrt((node[0] - new_node[0])**2 + (node[1] - new_node[1])**2) < 2.0]
                costs = {node: math.sqrt((node[0] - new_node[0])**2 + (node[1] - new_node[1])**2) for node in near_nodes}
                min_cost_node = min(near_nodes, key=lambda n: self.get_cost(n, costs) + costs[n])
                self.nodes.append(new_node)
                self.parent[new_node] = min_cost_node
                
                # Check if goal is reached
                for goal in self.goal_points:
                    if self.get_cost(new_node, costs) + costs[new_node] < self.goal_reached_threshold:
                        self.generate_path(new_node)
                        return
                
                # Publish the new node for visualization
                self.path_pub.publish(Point(new_node[0], new_node[1], 0))
                
    def get_cost(self, node, costs):
        # Calculate the cost of reaching a node using costs dictionary
        return costs[node] if node in costs else float("inf")
    
    def generate_path(self, goal_node):
        # Backtrack from goal to start to generate the path
        path = [goal_node]
        while path[-1] != self.start_point:
            path.append(self.parent[path[-1]])
        path.reverse()
        
        # Publish the planned path for visualization
        for node in path:
            self.path_pub.publish(Point(node[0], node[1], 0))
            rospy.sleep(0.1)

        # After the RRT* algorithm finishes planning the path
        self.generate_path(new_node)

        # Visualize the map and planned path
        self.visualize_map_and_path()

    def visualize_map_and_path(self):
        plt.figure(figsize=(10, 6))
        
        # Plot obstacles
        # (Add code to plot your obstacles if you have their coordinates)
        
        # Plot the nodes in the tree
        for node in self.nodes:
            plt.plot(node[0], node[1], 'go', markersize=3)
        
        # Plot the planned path
        path_points = []
        current_node = self.goal_points[0]
        while current_node != self.start_point:
            path_points.append(current_node)
            current_node = self.parent[current_node]
        path_points.append(self.start_point)
        
        path_x = [point[0] for point in path_points]
        path_y = [point[1] for point in path_points]
        plt.plot(path_x, path_y, 'r-')
        
        # Set labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Planned Path using RRT*')
        
        plt.grid(True)
        plt.show()


        
if __name__ == "__main__":
    planner = RRTStarPathPlanner()
    planner.rrt_star_planner()
