import matplotlib.pyplot as plt
import numpy as np
import random
import time
from enum import Enum
import math


class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STRAIGHT = "STRAIGHT"

class LightColor(Enum):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"


class Car:
    def __init__(self, spawn_node, max_acceleration=3, route=None): # Route default to None
        self.max_acceleration = max_acceleration
        self.route = route
        self.spawn_node = spawn_node
        self.current_lane = None;

        # position

        self.x = spawn_node.x
        self.y = spawn_node.y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def driving_behavior(self):
       pass


class Spawn_Node:
    def __init__(self, x, y, parent_segment: RoadSegment, spawn_chance=2, arrival_chance=2):
        self.x = x # Added x coordinate
        self.y = y # Added y coordinate
        self.spawn_chance = spawn_chance/300
        self.arrival_chance = arrival_chance
        self.parent_segment = parent_segment;



class Route:
    def __init__(self, starting_node, ending_node):
        # --- CHANGE 1: Cleaned up __init__ ---
        # We store the start and end nodes.
        self.start_node = starting_node
        self.end_node = ending_node

        # This will store the final list of RoadSegment objects
        self.traveled_segments = []

        # This will store the final calculated time (or 'weight')
        self.total_weight = math.inf

        # These are temporary variables used just for the pathfinding.
        self.unvisited_nodes = []
        # path_dict will be structured like:
        # { node_object: {"Shortest Distance": 0, "Previous Node": None}, ... }
        self.path_dict = {}
        # self.travel_time = None # This is now self.total_weight

    def find_path(self, network):
        # --- CHANGE 2: Correct Data Structure Initialization ---
        # The dictionary MUST be keyed by the node object itself.
        for node in network.nodes:
            # Add all nodes to the unvisited list
            self.unvisited_nodes.append(node)
            # Initialize all nodes with infinity distance
            self.path_dict[node] = {"Shortest Distance": math.inf, "Previous Node": None}

        # Set the starting node's distance to 0
        if self.start_node in self.path_dict:
            self.path_dict[self.start_node]["Shortest Distance"] = 0
        else:
            print("Error: Start node not in network.")
            return # Cannot find a path

        # --- CHANGE 3: The Main Dijkstra's Loop ---
        while self.unvisited_nodes:

            # --- CHANGE 4: Find the unvisited node with the smallest distance ---
            current_node = None
            min_dist = math.inf

            for node in self.unvisited_nodes:
                dist = self.path_dict[node]["Shortest Distance"]
                if dist < min_dist:
                    min_dist = dist
                    current_node = node

            # If current_node is None, no path exists (unreachable)
            if current_node is None:
                print("No path found.")
                break

            # --- CHANGE 5: Check for Completion & Remove Node ---
            # If we've reached the end node, we're done!
            if current_node == self.end_node:
                self.total_weight = self.path_dict[current_node]["Shortest Distance"]
                self.reconstruct_path() # Build the final path
                print(f"Path found! Total weight: {self.total_weight}")
                break

            # Remove the current node from the unvisited list
            self.unvisited_nodes.remove(current_node)

            # --- CHANGE 6: Check all neighbors (outgoing segments) ---
            for segment in current_node.outgoing_segments:
                neighbor = segment.node_b

                # We only care about neighbors we haven't visited yet
                if neighbor in self.unvisited_nodes:

                    # --- CHANGE 7: Calculate new distance ---
                    # The distance to this neighbor is:
                    # (current node's shortest distance) + (weight of the segment connecting them)
                    new_dist = self.path_dict[current_node]["Shortest Distance"] + segment.weight

                    # --- CHANGE 8: Update if this is a shorter path ---
                    if new_dist < self.path_dict[neighbor]["Shortest Distance"]:
                        # We found a shorter route to this neighbor!
                        self.path_dict[neighbor]["Shortest Distance"] = new_dist
                        self.path_dict[neighbor]["Previous Node"] = current_node

    def reconstruct_path(self):
        # --- CHANGE 9: Added Path Reconstruction ---
        # This private method works backward from the end_node
        # to build the final list of segments.

        path = []
        current_node = self.end_node

        # Keep looping as long as we have a "Previous Node"
        while self.path_dict[current_node]["Previous Node"] is not None:
            prev_node = self.path_dict[current_node]["Previous Node"]

            # Find the segment that connects prev_node to current_node
            # (This is inefficient, but clear. Can be optimized later)
            found_segment = None
            for segment in prev_node.outgoing_segments:
                if segment.node_b == current_node:
                    found_segment = segment
                    break

            if found_segment:
                path.append(found_segment)

            current_node = prev_node # Move one step back

        # The path was built backward (end to start), so we reverse it
        path.reverse()
        self.traveled_segments = path
        # You can print the path for debugging:
        # print("Path segments:", [f"{s.node_a.x},{s.node_a.y} -> {s.node_b.x},{s.node_b.y}" for s in self.traveled_segments])



