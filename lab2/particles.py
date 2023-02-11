import random
import math

# initialize particle count
num_particles = 100

# initialize x, y, and theta for each particle
particles = [[0, 0, 0] for i in range(num_particles)]

# initialize weight for each particle
weight = 1 / num_particles

# lines
line1 = (0,0,0,40)
line2 = (0,40,40,40)
line3 = (40,40,40,0)
line4 = (40,0,0,0)

# draw 40cm square on display
print("drawLine:" + str(line1))
print("drawLine:" + str(line2))
print("drawLine:" + str(line3))
print("drawLine:" + str(line4))

# every 10cm update particle spread
for i in range(0,160,10):
    # when the robot rotates 90 degrees
    if i == 40 or i == 80 or i == 120 or i == 160:
        for particle in particles:
            # random rotation error when turning
            g = random.gauss(0, 5)

            # theta_new = theta + alpha + g
            particle[2] += 90 + g

    # for driving straight
    else:
        for particle in particles:
                # random distance error when driving straight
                e = random.gauss(0, 3)

                # x_new = x + (D + e)cos(theta)
                particle[0] += ((10 + e) * math.cos(particle[2]))

                # y_new = y + (D + e)sin(theta)
                particle[1] += ((10 + e) * math.sin(particle[2]))

                # random rotation error when driving straight
                f = random.gauss(0, 3)

                # theta_new = theta + f
                particle[2] += f

    print("drawParticles:" + str(particles))
