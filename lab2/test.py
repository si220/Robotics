import random
import math
import time

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


# every 10cm update particle spread
for i in range(0,480,120):
    """
    # when the robot rotates 90 degrees
    if i == 120 or i == 240 or i == 360 or i == 480:
        pass
    
        for j, particle in enumerate(particles):
            # random rotation error when turning
            g = random.gauss(0, 5)

            # theta_new = theta + alpha + g
            particles[j] = (particle[0], particle[1], particle[2] + 90 + g)

    """
    # for driving straight
    
    for j, particle in enumerate(particles):
        
        # random rotation error when driving straight
        f = random.gauss(0, 12)

        # theta_new = theta + f
        theta = particle[2] + f
        
        # random distance error when driving straight
        e = random.gauss(0, 10)

        # x_new = x + (D + e)cos(theta)
        x = particle[0] + ((120 + e) * math.cos(math.radians(particle[2])))

        # y_new = y + (D + e)sin(theta)
        y = particle[1] + ((0 + e) * math.sin(math.radians(particle[2])))

        particles[j] = (x, y, theta)
    print(particles)
    print ("drawParticles:" + str(particles))
    time.sleep(2)