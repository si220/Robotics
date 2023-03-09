import brickpi3
import random
import time
import math
import numpy as np 
BP = brickpi3.BrickPi3()

#current angle 
current_x = 0.084
current_y = 0.03
current_angle = 0

# initialize particle count
num_particles = 100

# initialize x, y, and theta for each particle
particles = [(0, 0, 0) for i in range(num_particles)]

# initialize weight for each particle
weight = 1 / num_particles

# restricting speed of motors
BP.set_motor_limits(BP.PORT_C, 50, 200)
BP.set_motor_limits(BP.PORT_D, 50, 200)

def turn(turn_degrees):
    #reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    degrees_to_encoder_ratio = 200/90
    encoder_angle = degrees_to_encoder_ratio * turn_degrees
    # turn angle_a degrees left
    BP.set_motor_position(BP.PORT_C, encoder_angle)
    BP.set_motor_position(BP.PORT_D, - encoder_angle) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
    time.sleep(1.5)
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

def update_angle(turn_angle):
    for j,particle in enumerate(particles):
        g = random.gauss(0,3)
        particles[j] = (particle[0], particle[1], particle[2] + turn_angle - g)

def move(x,y,distance):
    # reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

    distance_to_encoder_ratio = 166/10
    encoder_pos = distance_to_encoder_ratio * distance *100
    # drive 10cm in a straight line
    BP.set_motor_position(BP.PORT_D, encoder_pos)
    BP.set_motor_position(BP.PORT_C, encoder_pos)
    time.sleep(1.5)
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

def update_position(distance):
    for i, particle in enumerate(particles):
        # random rotation error when driving straight
        f = random.gauss(0, 3)

        # theta_new = theta + f
        theta = particle[2] + f

        e = random.gauss(0, 0.01)

        x_cord = particle[0] + ((distance + e) * math.cos(math.radians(particle[2])))

        y_cord = particle[1] + ((distance + e) * math.sin(math.radians(particle[2])))

        particles[i] = (x_cord, y_cord, theta)

def navigateToWaypoint(x, y, current_x, current_y, current_angle):
    distance = math.sqrt((current_x-x)**2 + (current_y-y)**2)
    d_angle = math.degrees(math.atan2((y-current_y),(x-current_x)))

    turn_degrees = d_angle - current_angle
    print("Turning by this amount:", turn_degrees)
    current_x = x
    current_y = y
    current_angle = d_angle
    print("New angle:", current_angle)
    # Turn to face waypoint
    #print(current_angle)
    turn(turn_degrees)
    update_angle(turn_degrees)

    # Move forward to waypoint
    #print(distance)
    move(x,y,distance)
    update_position(distance)

def waypoint(x,y,particles):
    mean = np.mean(particles, axis=0)
    print("Current Position:", mean)
    current_x = mean[0]
    current_y = mean[1]
    current_angle = mean[2]
    navigateToWaypoint(x,y,current_x,current_y,current_angle)
    mean = np.mean(particles, axis=0)

waypoint(0.084,0.03,particles)
waypoint(0.18,0.03,particles)
waypoint(0.18,0.054,particles)
waypoint(0.138,0.054,particles)
waypoint(0.138,0.168,particles)
waypoint(0.114,0.168,particles)
waypoint(0.114,0.084,particles)
waypoint(0.084,0.084,particles)
waypoint(0.084,0.03,particles)

mean = np.mean(particles, axis=0)
print("Final Position:", mean)