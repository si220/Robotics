import brickpi3
import random
import time
import math
import numpy as np 
BP = brickpi3.BrickPi3()

#current angle 
current_angle = 0

# initialize particle count
num_particles = 100

# initialize x, y, and theta for each particle
particles = [(0, 0, 0) for i in range(num_particles)]

# initialize weight for each particle
weight = 1 / num_particles

# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

def turn(angle, turn_degrees):
    angle_a = math.degrees(turn_degrees)
    # reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    ratio_a = 200/90
    position_a = ratio_a * angle_a
    if angle_a > 0:
        # turn angle_a degrees left
        BP.set_motor_position(BP.PORT_D, -position_a) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
        BP.set_motor_position(BP.PORT_C, position_a)

    else: 
        # turn angle_a degrees right
        BP.set_motor_position(BP.PORT_D, position_a) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
        BP.set_motor_position(BP.PORT_C, -position_a)

    time.sleep(1.5)

    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

    for j, particle in enumerate(particles):
        # random rotation error when turning
        g = random.gauss(0, 3)

        # theta_new = theta + alpha + g
        particles[j] = (particle[0], particle[1], math.degrees(angle) + g)

def move(x,y,distance):
    # reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    ratio_d = 166/10
    position_d = ratio_d * distance*100
    # drive 10cm in a straight line
    BP.set_motor_position(BP.PORT_D, position_d)
    BP.set_motor_position(BP.PORT_C, position_d)

    time.sleep(1.5)
        
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 3)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 0.01)

        x_cord = particle[0] + ((distance + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y_cord = particle[1] + ((distance + e) * math.sin(math.radians(particle[2])))     
             
        particles[j] = (x_cord, y_cord, theta)

def navigateToWaypoint(x, y, current_angle):
    distance = math.sqrt((x)**2 + (y)**2)
    angle = math.atan2(y,x)
    turn_degrees = angle - current_angle
    current_angle = angle
    # Turn to face waypoint
    print(math.degrees(angle))
    turn(angle, turn_degrees)

    # Move forward to waypoint
    print(distance)
    move(x,y,distance)

    return current_angle

current_angle = navigateToWaypoint(-0.3,0.3, current_angle)
mean = np.mean(particles, axis=0)
print(mean[0]*100, mean[1]*100, mean[2])

current_angle = navigateToWaypoint(0.3,-0.3, current_angle)
mean = np.mean(particles, axis=0)
print(mean[0]*100, mean[1]*100, mean[2])

current_angle = navigateToWaypoint(-0.3,-0.3, current_angle)
mean = np.mean(particles, axis=0)
print(mean[0]*100, mean[1]*100, mean[2])

current_angle = navigateToWaypoint(0.3,0.3, current_angle)
mean = np.mean(particles, axis=0)
print(mean[0]*100, mean[1]*100, mean[2])
