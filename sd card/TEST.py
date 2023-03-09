import brickpi3
import time
import random
import math
import numpy as np
BP = brickpi3.BrickPi3()

# initialize particle count
num_particles = 100

# initialize x, y, and theta for each particle
particles = [(100, 580, 0) for i in range(num_particles)]

# initialize weight for each particle
weight = 1 / num_particles

# lines
line1 = (100,100,100,580)
line2 = (100,580,580,580)
line3 = (580,580,580,100)
line4 = (580,100,100,100)

# draw 40cm square on display
print ("drawLine:" + str(line1))
print ("drawLine:" + str(line2))
print ("drawLine:" + str(line3))
print ("drawLine:" + str(line4))

print ("drawParticles:" + str(particles))
time.sleep(1)

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