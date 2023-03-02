import brickpi3
import time
import random
import math
import numpy as np
BP = brickpi3.BrickPi3()
from canvas import *

# initialize particle count
num_particles = 100

# initialize x, y, and theta for each particle
particles = [(0, 0, 0) for i in range(num_particles)]

# initialize weight for each particle
weights = [(1 / num_particles) for i in range(num_particles)]

# probabilistic motion
def drive(x, y, theta, D, alpha, e, f, g):
    if alpha == 0:
        x = x + (D + e) * math.cos(theta)
        y = y + (D + e) * math.sin(theta)
        theta = theta + f
    else:
        x = x
        y = y
        theta = theta + alpha + g
        
    return x, y, theta


walls = [((0, 0), (0, 168)), # wall a
        ((0, 168), (84, 168)), # wall b
        ((84, 126), (84, 210)), # wall c
        ((84, 210), (168, 210)), # wall d
        ((168, 210), (168, 84)), # wall e
        ((168, 84), (210, 84)), # wall f
        ((210, 84), (210, 0)), # wall g
        ((210, 0), (0, 0))] # wall h


def closest_wall(x, y, theta, walls):
    m_min = float('inf')

    for wall in walls:
        # Get the endpoints of the line segment
        x1, y1 = wall[0]
        x2, y2 = wall[1]

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


def calculate_likelihood(x, y, theta, z, m):
    # find out which wall robot will hit and expected depth measurement
    m = closest_wall(x, y, theta, walls)
    # calculate likelihood using a gaussian distribution with a standard deviation of 3
    # add a constant of 0.1 for robustness
    likelihood = math.exp(-((z - m) ** 2) / (2 * 3 ** 2)) + 0.1
    return likelihood


def update(D, alpha, e, f, g, z, canvas):
    # perform probabilistic motion for each particle
    for i in range(num_particles):
        x, y, theta = particles[i]
        x, y, theta = drive(x, y, theta, D, alpha, e, f, g)
        particles[i] = (x, y, theta)
    
    # update weights based on sensor reading and distance to nearest wall
    for i in range(num_particles):
        x, y, theta = particles[i]
        m = closest_wall(x, y, theta, walls)
        w = calculate_likelihood(x, y, theta, z, m)
        weights[i] *= w

    # update particle positions on canvas
    for i in range(num_particles):
        x, y, theta = particles[i]
        canvas.drawParticles([(x, y, theta)])
    
    # normalize weights and resample particles
    # weight = normalize_weights(weight)
    # particles = resample_particles(particles, weight)


# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

for i in range(4):
    # reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    # drive 10cm in a straight line
    BP.set_motor_position(BP.PORT_D, 160)
    BP.set_motor_position(BP.PORT_C, 160)

    time.sleep(1)
        
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

    # D = 50, alpha = 0, e = 3, f = 5, g = 4, z = 52, 
    update(10, 0, 3, 5, 4, 52, canvas)
