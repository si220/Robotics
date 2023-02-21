#!/usr/bin/env python 
# Some suitable functions and data structures for drawing a map and particles
import brickpi3
import time
import random
import math

BP = brickpi3.BrickPi3()
# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

# Functions to generate some dummy particles data:
def calcX(x, theta, D, alpha, e):
    if alpha==0:
        x = x + (D + e) * math.cos(math.radians(theta))
    else:
        x = x
    return x

def calcY(y, theta, D, alpha, e):
    if alpha==0:
        y = y + (D + e) * math.sin(math.radians(theta))
    else:
        y = y
    return y

def calcTheta(theta, alpha, f, g):
    if alpha==0:
        theta = theta + f
    else: 
        theta = theta + alpha + g
    return theta

# A Canvas class for drawing a map and particles:
# 	- it takes care of a proper scaling and coordinate transformation between
#	  the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def drawLine(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        print ("drawLine:" + str((x1,y1,x2,y2)))

    def drawParticles(self,data, weights):
        display = [(self.__screenX(d[0]),self.__screenY(d[1])) + (d[2], weights[i]) for i, d in enumerate(data)];
        print ("drawParticles:" + str(display));

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
    def __init__(self, canvas):
        self.walls = [];
        self.canvas = canvas

    def add_wall(self,wall):
        self.walls.append(wall);

    def clear(self):
        self.walls = [];

    def draw(self):
        for wall in self.walls:
            self.canvas.drawLine(wall);

# Simple Particles set
class Particles:
    def __init__(self, canvas, n_particles=100, initial_pos=(0, 0, 0)):
        self.n = n_particles;
        self.canvas = canvas
        self.data = [initial_pos for i in range(self.n)]
        self.weights = [1/self.n for i in range(self.n)]

    def update_spread(self, robot_pos, D, alpha):
        for i in range(self.n):
            e = random.gauss(0, 1)
            f = random.gauss(0, 1)
            g = random.gauss(0, 1)
            self.data[i] = (calcX(robot_pos.x, robot_pos.theta, D, alpha, e),
                            calcY(robot_pos.y, robot_pos.theta, D, alpha, e),
                            calcTheta(robot_pos.theta, alpha, f, g))

    def update_weights(self, map, sensor_reading):
        for i in range(self.n):
            w = calculate_likelihood(self.data[i], sensor_reading, map)
            self.weights[i] *= w
        sum = sum(self.weights)
        for i in range(self.n):
            self.weights[i] /= sum
    
    def resample(self):
        cdf = []
        counter = 0
        list_copy = self.data
        for i in range(self.n):
            counter+=self.weights[i]
            cdf[i] = counter
        for k in range(self.n):
            random_n = random.random()
            j = 0
            while random_n > cdf[j]:
                j+=1
            self.data[k] = list_copy[j]
            self.weights[k] = 0.01
        
    def draw(self):
        self.canvas.drawParticles(self.data, self.weights);

class Robot_position:
    def __init__(self, initial_pos=(0, 0, 0)):
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.theta = initial_pos[2]

    def update(self, particles):
        sum_x=0; sum_y=0; sum_theta=0
        for i in range(len(particles.data)):
            sum_x += particles.weights[i]*particles.data[i][0]
            sum_y += particles.weights[i]*particles.data[i][1]
            sum_theta += particles.weights[i]*particles.data[i][2]
        self.x=sum_x; self.y=sum_y; self.theta=sum_theta

def closest_wall_distance(pos, map):
    x=pos[0]; y=pos[1]; theta=pos[2]
    m_min = float('inf')

    for wall in map.walls:
        # Get the endpoints of the line segment
        x1, y1 = wall[0], wall[1]
        x2, y2 = wall[2], wall[3]

        # Calculate m
        m = ((y2 - y1) * (x1 - x) - (x2 - x1) * (y1 - y)) / ((y2 - y1) * math.cos(theta) - (x2 - x1) * math.sin(theta))

        # If the line segment is behind the robot, skip it
        if m < 0:
            continue

        # Calculate the intersection point of the line segment and the line of sight of the robot
        xi = x + m * math.cos(theta)
        yi = y + m * math.sin(theta)

        # If the intersection point is not on the line segment, skip it
        if xi < min(x1, x2) or xi > max(x1, x2) or yi < min(y1, y2) or yi > max(y1, y2):
            continue

        # Calculate the distance from the robot to the line segment
        distance = math.sqrt((xi - x) ** 2 + (yi - y) ** 2)

        # Update the minimum distance
        m_min = min(m_min, distance)

    return m_min

def calculate_likelihood(pos, sensor_reading, map):
    # find out which wall robot will hit and expected depth measurement
    m = closest_wall_distance(pos, map)
    # calculate likelihood using a gaussian distribution with a standard deviation of 3
    # add a constant of 0.1 for robustness
    likelihood = math.exp(-((sensor_reading - m) ** 2) / (2 * 3 ** 2)) + 0.1
    return likelihood

def turn(turn_degrees):
    #reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    degrees_to_encoder_ratio = 200/90
    encoder_angle = degrees_to_encoder_ratio * turn_degrees
    # turn angle_a degrees left
    BP.set_motor_position(BP.PORT_C, encoder_angle)
    BP.set_motor_position(BP.PORT_D, - encoder_angle) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
    time.sleep(0.5)
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

def move_forward(distance):
    # reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

    distance_to_encoder_ratio = 166/10
    encoder_pos = distance_to_encoder_ratio * distance *100
    # drive 10cm in a straight line
    BP.set_motor_position(BP.PORT_D, encoder_pos)
    BP.set_motor_position(BP.PORT_C, encoder_pos)
    time.sleep(0.5)
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

def navigateToWaypoint(x, y, current_pos):
    distance = math.sqrt((current_pos.x-x)**2 + (current_pos.y-y)**2)
    d_angle = math.degrees(math.atan2((y-current_pos.y),(x-current_pos.x)))

    turn_degrees = d_angle - current_pos.theta
    print("Turning by this amount:", turn_degrees)
    current_angle = d_angle
    print("New angle:", current_angle)
    # Turn to face waypoint
    turn(turn_degrees)
    # Move forward to waypoint
    move_forward(distance)
    return distance, turn_degrees

def Navigate_and_update_particles(x, y, current_pos, particles):
    D, alpha= navigateToWaypoint(x, y, current_pos)
    particles.update_spread(current_pos, D, alpha)

def fetch_sensor_readings():
    pass