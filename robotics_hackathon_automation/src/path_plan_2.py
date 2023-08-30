#!/usr/bin/env python3

# this is by shlok
# doesn't work currently

import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import obstacle_detection as obsdet  # Import the obstacle detection module

# Parameters
start = (-5.06, -3.12)
goal = (5.18, -2.19)
max_iterations = 1000
step_size = 0.5

# Initialize RRT*
rrt_tree = {start: None}

def generate_random_point():
    x = np.random.uniform(-5.06, 5.18)
    y = np.random.uniform(-3.12, 2.51)
    return x, y

def nearest_neighbor(tree, point):
    nearest = None
    min_dist = float('inf')
    for node in tree:
        dist = np.sqrt((node[0] - point[0])*2 + (node[1] - point[1])*2)
        if dist < min_dist:
            min_dist = dist
            nearest = node
    return nearest

def new_point(from_node, to_node):
    angle = np.arctan2(to_node[1] - from_node[1], to_node[0] - from_node[0])
    new_x = from_node[0] + step_size * np.cos(angle)
    new_y = from_node[1] + step_size * np.sin(angle)
    return new_x, new_y

def cost(node):
    return np.sqrt((node[0] - start[0])*2 + (node[1] - start[1])*2)

def find_near_nodes(tree, new_node, radius):
    near_nodes = []
    for node in tree:
        dist = np.sqrt((node[0] - new_node[0])*2 + (node[1] - new_node[1])*2)
        if dist < radius:
            near_nodes.append(node)
    return near_nodes

def rewire(tree, new_node, near_nodes):
    for near_node in near_nodes:
        if obsdet.isValidPoint(near_node[0], near_node[1], new_node[0], new_node[1]):
            new_cost = cost(new_node) + np.sqrt((new_node[0] - near_node[0])*2 + (new_node[1] - near_node[1])*2)
            if new_cost < cost(near_node):
                tree[near_node] = new_node

# RRT* Algorithm
for _ in range(max_iterations):
    random_point = generate_random_point()
    nearest_node = nearest_neighbor(rrt_tree, random_point)
    new_node = new_point(nearest_node, random_point)
    
    if obsdet.isValidPoint(nearest_node[0], nearest_node[1], new_node[0], new_node[1]):
        near_nodes = find_near_nodes(rrt_tree, new_node, radius=3*step_size)
        rrt_tree[new_node] = nearest_node
        rewire(rrt_tree, new_node, near_nodes)

# Extract path
path = []
current_node = goal
while current_node is not None:
    path.append(current_node)
    current_node = rrt_tree[current_node]

# Plot the result
for wall in obsdet.maze:  # Use the maze list from obstacle detection module
    x, y = wall.polygon.exterior.xy
    plt.plot(x, y, 'k')

for node, parent in rrt_tree.items():
    if parent is not None:
        plt.plot([parent[0], node[0]], [parent[1], node[1]], 'b')

for point in path:
    plt.plot(point[0], point[1], 'ro')

plt.plot(start[0], start[1], 'go', label='Start')
plt.plot(goal[0], goal[1], 'yo', label='Goal')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('RRT* Path Planning')
plt.show()