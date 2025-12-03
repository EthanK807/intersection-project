# Please paste your intersection code here.
# I'm ready to help you debug, optimize, or explain it!

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




def main():
    def simulate(intersection, steps=300):
        for t in range(steps):
            print(f"\n--- Time step {t} ---")

            # filles lanes with cars


            for road in intersection.road_segments:
                if len(road.spawn_nodes) > 0:
                    for spawn_node in road_segment.spawn_nodes:
                        if (random.random() < spawn_node.spawn_chance)
                            spawned_car = car(spawn_node, np.random.normal(3, 0.25))
                            # --- This is how you'd spawn a car ---
                            # 1. Pick a random spawn node from the road
                            # 2. Figure out a route (This is complex, placeholder for now)
                            # route = Route(spawn_node, ...)
                            arrival_node = None
                            while (true):
                                for spawn_node in network.road_segments.spawn_nodes:
                                    if (random.random() < spawn_node.arrival_chance)
                                        arrival_node = spawn_node
                                        break
                            assigned_route = route(spawned_car.spawn_node, arrival_node)
                            spawn_car.route = assigned_route


                    print(f"Car would spawn at {spawn_node.x}, {spawn_node.y}")


            # Update traffic lights (simple toggle)

            for road in intersection.road_segments: # FIX: Was intersection.roads, which doesn't exist
                for lane in road.lanes:
                    # FIX: Added 'if lane.traffic_light' to prevent crash
                    # Lanes not at an intersection won't have a light.
                    if lane.traffic_light and lane.traffic_light.color == LightColor.GREEN and r < 0.1/30:
                        lane.traffic_light.change_color(LightColor.RED) # FIX: Was .change()
                    elif lane.traffic_light and (r < 0.1/30): # FIX: Added 'if lane.traffic_light'
                        lane.traffic_light.change_color(LightColor.GREEN) # FIX: Was .change()

            # Move vehicles if light is green
            for road in intersection.road_segments: # FIX: Was intersection.roads
                for lane in road.lanes:
                    # FIX: 'len(lane.queue)' is correct syntax.
                    # FIX: Added 'if lane.traffic_light'
                    if lane.traffic_light and lane.traffic_light.color == LightColor.GREEN and len(lane.queue) != 0:
                        car = lane.vehicles.pop(0)  # car leaves the lane
                        print(f"{car} passed through {road.name} going {lane.direction}")

            # moves the cars through the intersection
            for road in intersection.road_segments: # FIX: Was intersection.roads
                for lane in road.lanes: # FIX: Was roads.lanes
                    for cars in lane.queue: # FIX: Was lanes.queue
                        pass # Added 'pass' to make the loop valid


            time.sleep(.0333)  # wait one second per step (for realism)


class Network:
    def __init__(self):
        self.nodes = []
        self.road_segments = []

    def connect_nodes(self, speed_limit, spawn_node_density, num_lanes, node_a: 'Node', node_b: 'Node', one_way: Boolean):
        # 1. Create the first road segment (from A to B)
        segment_ab = RoadSegment(num_lanes, node_a, node_b, self, speed_limit, spawn_node_density)
        # 2. Add the first segment to the list
        self.road_segments.append(segment_ab)
        # --- Add segment to the nodes ---
        node_a.add_segment(segment_ab)
        node_b.add_segment(segment_ab)


        # 3. Check if it's a two-way connection
        if not one_way:
            # 4. If it's two-way, create the second road segment (from B to A)
            segment_ba = RoadSegment(num_lanes, node_b, node_a, self, speed_limit, spawn_node_density)
            # 5. Add the second segment to the list
            self.road_segments.append(segment_ba)
            # --- Add segment to the nodes ---
            node_a.add_segment(segment_ba)
            node_b.add_segment(segment_ba)

        node_a.update_characteristics()
        node_b.update_characteristics()

    def node_creation(self):
        pass




class Node:
    def __init__(self, x, y, parent_network: 'Network'):
        self.x = x
        self.y = y
        self.segments = [] # Renamed from 'connections' to store RoadSegments
        self.outgoing_segments = []
        self.parent_network = parent_network;


    def get_node_type(self) -> str:
        """Determines the type of node based on the number of connections."""
        num_connections = len(self.segments) # Now correctly uses self.segments

        if num_connections <= 2:
            return "Transition Node"
        elif num_connections >= 3:
            return "Intersection Node"
        else:
            return "Isolated Node"

    def update_characteristics(self):
        """Sets attributes like spawn_chance based on the node's type."""
        node_type = self.get_node_type()

        if node_type == "Transition Node":

            self.is_decision_point = True
            self.is_traffic_controlled = False
            self.outgoing_segments = []
            for segment in self.segments:
                if segment.node_a == self:
                    self.outgoing_segments.append(segment)

        elif node_type == "Intersection Node":
            # A decision point, traffic light may be here, but no new cars spawn mid-intersection

            self.is_decision_point = True
            self.is_traffic_controlled = True

            self.outgoing_segments = []
            for segment in self.segments:
                if segment.node_a == self:
                    self.outgoing_segments.append(segment)

            # --- This is the new logic you asked for ---
            # Find all INCOMING lanes and give them a traffic light
            for segment in self.segments:
                # If this node is the DESTINATION of the segment, it's an incoming road
                if segment.node_b == self:
                    # This road segment is coming INTO this intersection node
                    # (We assume initialize_lanes() has been called already)
                    for lane in segment.lanes:
                        # Assign a new traffic light to each incoming lane
                        if lane.traffic_light is None: # Only add one if it doesn't exist
                            lane.assign_light(TrafficLight())
                            # You could add a print statement here for debugging
                            # print(f"Assigned light to lane in segment ending at {self.x}, {self.y}")


    def add_connection(self, node):
        self.connections.append(node)

    def add_segment(self, segment):
        """Stores a reference to a connected RoadSegment"""
        if segment not in self.segments:
            self.segments.append(segment)

'''Spawn chance passed as % per second'''

class Spawn_Node:
    def __init__(self, x, y, parent_segment: RoadSegment, spawn_chance=2, arrival_chance=2):
        self.x = x # Added x coordinate
        self.y = y # Added y coordinate
        self.spawn_chance = spawn_chance/300
        self.arrival_chance = arrival_chance
        self.parent_segment = parent_segment;


class TrafficLight:
    def __init__(self, color=LightColor.RED):
        self.color = color
        self.parent_intersection_node = Null;

    def change_color(self, color):
        self.color = color # Was color.upper(), which would crash on an Enum

class Car:
    def __init__(self, spawn_node, max_acceleration=3, route=None): # Route default to None
        self.max_acceleration = max_acceleration
        self.route = route
        self.spawn_node = spawn_node
        self.current_lane = Null;

        # position

        self.x = spawn_node.x
        self.y = spawn_node.y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    def driving_behavior(self):
        if ()





# Detects if there is a car in front of it.



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


class Lane:
    def __init__(self):
        self.direction_options = []
        self.queue = []
        self.traffic_light = None

    def add_car(self, car):
        self.queue.append(car)

    def add_direction(self, direction):
        self.direction_options.append(direction)

    def assign_light(self, light):
        self.traffic_light = light

''' Speed is done in meters per second
    spawn_chance done in % per second
    entry_chance must add up to 100 at an intersection
'''

class RoadSegment:
    def __init__(self, num_lanes, node_a, node_b, parent_network: Network, speed_limit=15, spawn_node_density=12):
        self.num_lanes = num_lanes # Moved this up
        if (self.num_lanes > 10):
            raise ValueError("The number of lanes must be below 10.")

        self.lanes = []
        self.speed_limit = speed_limit
        self.spawn_node_density = spawn_node_density
        self.node_a = node_a
        self.node_b = node_b
        self.length = abs(math.sqrt((node_a.x - node_b.x)**2 + (node_a.y - node_b.y)**2))
        self.weight = self.length / self.speed_limit

        # --- New additions for spawn nodes ---
        self.spawn_nodes = [] # List to hold the spawn nodes
        self.spawn_chance = 0.1 # A default spawn chance for the whole road
        self.create_spawn_nodes() # Create the nodes when the road is created
        # --- End new additions ---


    def create_spawn_nodes(self):
        """Creates evenly-spaced spawn nodes along the road segment."""
        # FIX: Was 'spawn_density', which is not defined. Use 'self.spawn_node_density'
        if self.length == 0 or self.spawn_node_density == 0 or self.spawn_node_density > self.length:
            return # Cannot create nodes on a zero-length road or with zero density

        # 1. Calculate N (Number of nodes)
        num_nodes = math.floor(self.length / self.spawn_node_density)
        if num_nodes == 0:
            return # Road is too short to fit any nodes

        # 2. Calculate segment_length (for centering)
        segment_length = self.length / (num_nodes + 1)

        # 3. Calculate the road's unit vector (direction)
        vec_x = self.node_b.x - self.node_a.x
        vec_y = self.node_b.y - self.node_a.y
        unit_x = vec_x / self.length
        unit_y = vec_y / self.length

        # 4. Place the nodes
        for i in range(1, num_nodes + 1):
            # Distance from node_a
            dist = i * segment_length

            # Calculate coordinates
            spawn_x = self.node_a.x + (dist * unit_x)
            spawn_y = self.node_a.y + (dist * unit_y)

            # Create and store the new node
            new_node = Spawn_Node(spawn_x, spawn_y)
            self.spawn_nodes.append(new_node)
            # print(f"Created spawn node at ({spawn_x:.2f}, {spawn_y:.2f})") # For debugging


    def initialize_lanes(self):

        # FIX: .get_node_type is a method, must be called with ()
        if (self.node_b.get_node_type() == "Intersection Node"):
            # FIX: self.num_lanes is an int. Must use range(self.num_lanes)
            for i in range(self.num_lanes):
                self.lanes.append(Lane())
                # FIX: .upper() is a method of the string.
                # FIX: L, S, R must be strings: "L", "S", "R"
                lanes_input = upper(input(
                    f'You have {self.num_lanes} lanes. This is lane {i} from the left. Which directions would you like a driver to be able to turn in this lane? (ex. straight right)'))
                counter = 0

                for char in lanes_input: # FIX: Was 'lanes'
                    if (char == "L") & (lanes_input[counter:counter+5] == "LEFT"):
                        self.lanes[i].add_direction(Direction.LEFT)
                    if (char == "S") & (lanes_input[counter:counter+8] == "STRAIGHT"):
                        self.lanes[i].add_direction(Direction.STRAIGHT)
                    if (char == "R") & (lanes_input[counter:counter+6] == "RIGHT"):
                        self.lanes[i].add_direction(Direction.RIGHT)

                    counter += 1


    def add_node(self, node):
        self.nodes.append(node)


