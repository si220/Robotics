import brickpi3
import numpy as np
import time
import random
import math
import montecarlo_classes as mc
BP = brickpi3.BrickPi3()

canvas = mc.Canvas();	# global canvas we are going to draw on
mymap = mc.Map(canvas);
# Definitions of walls
mymap.add_wall((0,0,0,168));        # a: O to A
mymap.add_wall((0,168,84,168));     # b: A to B
mymap.add_wall((84,126,84,210));    # c: C to D
mymap.add_wall((84,210,168,210));   # d: D to E
mymap.add_wall((168,210,168,84));   # e: E to F
mymap.add_wall((168,84,210,84));    # f: F to G
mymap.add_wall((210,84,210,0));     # g: G to H
mymap.add_wall((210,0,0,0));        # h: H to O
mymap.draw();

# initialize particle count
num_particles = 100
initial_robot_position = (84, 30, 0)
# initialize x, y, and theta for each particle
particles = mc.Particles(canvas, n_particles=100, initial_pos = initial_robot_position)
robot_pos = mc.Robot_position(initial_pos = initial_robot_position)
print(robot_pos.x, robot_pos.y, robot_pos.theta)

particles.draw()
time.sleep(2)
particles.update_spread(robot_pos, 100, 0)
particles.update_weights(mymap, 10)
robot_pos.update(particles)
print(robot_pos.x, robot_pos.y, robot_pos.theta)
particles.draw()

time.sleep(2)

particles.update_spread(robot_pos, 0, 180)
particles.update_weights(mymap, 10)
robot_pos.update(particles)
print(robot_pos.x, robot_pos.y, robot_pos.theta)
particles.draw()

time.sleep(2)

particles.update_spread(robot_pos, 150, 0)
particles.update_weights(mymap, 10)
robot_pos.update(particles)
print(robot_pos.x, robot_pos.y, robot_pos.theta)
particles.draw()
'''
# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

# every 10cm update particle spread
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

    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 1)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 5)

        # x_new = x + (D + e)cos(theta)
        x = particle[0] + ((120 + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y = particle[1] + ((120 + e) * math.sin(math.radians(particle[2])))

        particles[j] = (x, y, theta)
    #print(particles)
    print ("drawParticles:" + str(particles))
    time.sleep(1)

# reset encoder position in between each movement
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

# turn 90 degrees
BP.set_motor_position(BP.PORT_D, -205) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
BP.set_motor_position(BP.PORT_C, 205)

time.sleep(1)
        
# check if motor velocity = 0
while BP.get_motor_status(BP.PORT_D)[3] != 0:
    pass

for j, particle in enumerate(particles):
    # random rotation error when turning
    g = random.gauss(0, 5)

    # theta_new = theta + alpha + g
    particles[j] = (particle[0], particle[1], particle[2] + 90 + g)
print ("drawParticles:" + str(particles))
time.sleep(1)

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
    
    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 1)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 5)

        # x_new = x + (D + e)cos(theta)
        x = particle[0] - ((120 + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y = particle[1] - ((120 + e) * math.sin(math.radians(particle[2])))

        particles[j] = (x, y, theta)
    #print(particles)
    print ("drawParticles:" + str(particles))
    time.sleep(1)

# reset encoder position in between each movement
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

# turn 90 degrees
BP.set_motor_position(BP.PORT_D, -205) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
BP.set_motor_position(BP.PORT_C, 205)

time.sleep(1)
        
# check if motor velocity = 0
while BP.get_motor_status(BP.PORT_D)[3] != 0:
    pass
for j, particle in enumerate(particles):
    # random rotation error when turning
    g = random.gauss(0, 5)

    # theta_new = theta + alpha + g
    particles[j] = (particle[0], particle[1], particle[2] - 90 - g)
print ("drawParticles:" + str(particles))
time.sleep(1)

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

    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 1)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 5)

        # x_new = x + (D + e)cos(theta)
        x = particle[0] - ((120 + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y = particle[1] - ((120 + e) * math.sin(math.radians(particle[2])))

        particles[j] = (x, y, theta)
    #print(particles)
    print ("drawParticles:" + str(particles))
    time.sleep(1)

# reset encoder position in between each movement
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

# turn 90 degrees
BP.set_motor_position(BP.PORT_D, -205) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
BP.set_motor_position(BP.PORT_C, 205)

time.sleep(1)
        
# check if motor velocity = 0
while BP.get_motor_status(BP.PORT_D)[3] != 0:
    pass

for j, particle in enumerate(particles):
    # random rotation error when turning
    g = random.gauss(0, 5)

    # theta_new = theta + alpha + g
    particles[j] = (particle[0], particle[1], particle[2] - 90 - g)
print ("drawParticles:" + str(particles))
time.sleep(1)

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
    
    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 1)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 5)

        # x_new = x + (D + e)cos(theta)
        x = particle[0] - ((120 + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y = particle[1] - ((120 + e) * math.sin(math.radians(particle[2])))

        particles[j] = (x, y, theta)
    #print(particles)
    print ("drawParticles:" + str(particles))
    time.sleep(1)

# reset encoder position in between each movement
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

# turn 90 degrees
BP.set_motor_position(BP.PORT_D, -205) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
BP.set_motor_position(BP.PORT_C, 205)

time.sleep(1)
        
# check if motor velocity = 0
while BP.get_motor_status(BP.PORT_D)[3] != 0:
    pass

for j, particle in enumerate(particles):
    # random rotation error when turning
    g = random.gauss(0, 5)

    # theta_new = theta + alpha + g
    particles[j] = (particle[0], particle[1], particle[2] - 90 - g)
print ("drawParticles:" + str(particles))
time.sleep(1)

mean = np.mean(particles, axis=0)
print(mean)
'''