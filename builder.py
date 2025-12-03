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


class TrafficLight:
    def __init__(self, color=LightColor.RED):
        self.color = color
        self.parent_intersection_node = None;

    def change_color(self, color):
        self.color = color # Was color.upper(), which would crash on an Enum
