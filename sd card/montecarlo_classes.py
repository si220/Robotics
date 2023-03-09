# Some suitable functions and data structures for drawing a map and particles
import brickpi3
import time
import random
import math

BP = brickpi3.BrickPi3()
# BP.SENSOR_TYPE.NXT_ULTRASONIC specifies that the sensor will be an NXT ultrasonic sensor.
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC)
# restricting speed of motors
BP.set_motor_limits(BP.PORT_D, 50, 200)
BP.set_motor_limits(BP.PORT_C, 50, 200)

# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
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

def calcX(x, theta, D, e):
    x = x + (D + e) * math.cos(math.radians(theta))
    return x

def calcY(y, theta, D, e):
    y = y + (D + e) * math.sin(math.radians(theta))
    return y

def calcTheta(theta, turn_degrees,f,g):
    if abs(turn_degrees) < 2:
        theta = theta + f
    else: 
        theta = theta + turn_degrees + g
    return theta

def closest_wall_distance(particle_pos, map):
    x = particle_pos[0]
    y = particle_pos[1]
    theta = particle_pos[2]
    m_min = float('inf')

    for wall in map.walls:
        # Get the endpoints of the line segment
        x1, y1 = wall[0], wall[1]
        x2, y2 = wall[2], wall[3]

        # Calculate m
        m = ((y2 - y1) * (x1 - x) - (x2 - x1) * (y1 - y)) / ((y2 - y1) * math.cos(math.radians(theta)) - (x2 - x1) * math.sin(math.radians(theta)))

        # If the line segment is behind the robot, skip it
        if m < 0:
            continue

        # Calculate the intersection point of the line segment and the line of sight of the robot
        xi = x + m * math.cos(math.radians(theta))
        yi = y + m * math.sin(math.radians(theta))

        # If the intersection point is not on the line segment, skip it
        if xi < min(x1, x2) or xi > max(x1, x2) or yi < min(y1, y2) or yi > max(y1, y2):
            continue

        # Calculate the distance from the robot to the line segment
        distance = math.sqrt((xi - x) ** 2 + (yi - y) ** 2)

        # Update the minimum distance
        m_min = min(m_min, distance)

    return m_min

def calculate_Likelihood(particle_pos, sensor_reading, map):
    # find out which wall robot will hit and expected depth measurement
    m = closest_wall_distance(particle_pos, map)
    # calculate likelihood using a gaussian distribution with a standard deviation of 3
    # add a constant of 0.1 for robustness
    likelihood = math.exp(-((sensor_reading - m) ** 2) / (2 * 3 ** 2)) + 0.005

    return likelihood

# Simple Particles set
class Particles:
    def __init__(self, canvas, n_particles=100, initial_pos=(0, 0, 0)):
        self.n = n_particles
        self.canvas = canvas
        self.data = [initial_pos for i in range(self.n)]
        self.weights = [1/self.n for i in range(self.n)]
        
    def draw(self):
        self.canvas.drawParticles(self.data, self.weights)

    def update_spread(self, distance, turn_degrees):
        for i in range(self.n):
            e = random.gauss(0, 2)
            f = random.gauss(0, 2.5)
            g = random.gauss(0, 3.5)
            
            theta = calcTheta(self.data[i][2], turn_degrees, f, g)
            x = calcX(self.data[i][0], theta, distance, e)
            y = calcY(self.data[i][1], theta, distance, e)
            self.data[i] = (x, y, theta)

    def update_and_norm_weights(self, map, sensor_reading):
        for i in range(self.n):
            likelihood = calculate_Likelihood(self.data[i], sensor_reading, map)
            self.weights[i] *= likelihood
        s = sum(self.weights)
        for i in range(self.n):
            self.weights[i] /= s

    def resample(self):
        new_data = []
        cdf = [0]*self.n
        counter = 0
        for i in range(self.n):
            counter += self.weights[i]
            cdf[i] = counter
        for k in range(self.n):
            random_n = random.random()
            j = 0
            while random_n > cdf[j]:
                j += 1
            new_data.append(self.data[j])
        self.data = new_data
        self.weights = [1/self.n for i in range(self.n)]

class Robot_position:
    def __init__(self, initial_pos=(0, 0, 0)):
        self.x = initial_pos[0]
        self.y = initial_pos[1]
        self.theta = initial_pos[2]

    def update(self, particles):
        sum_x = 0
        sum_y = 0
        sum_theta = 0
        for i in range(len(particles.data)):
            sum_theta += particles.weights[i]*particles.data[i][2]
            sum_x += particles.weights[i]*particles.data[i][0]
            sum_y += particles.weights[i]*particles.data[i][1]
        self.x = sum_x
        self.y = sum_y
        self.theta = sum_theta

def turn(turn_degrees):
    #reset encoder position in between each movement
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

    degrees_to_encoder_ratio = 220/90 #210/90
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
    encoder_pos = distance_to_encoder_ratio * distance 
    # drive 10cm in a straight line
    BP.set_motor_position(BP.PORT_D, encoder_pos)
    BP.set_motor_position(BP.PORT_C, encoder_pos)
    time.sleep(0.5)
    # check if motor velocity = 0
    while BP.get_motor_status(BP.PORT_D)[3] != 0:
        pass

def navigateToWaypoint(x, y, current_pos, particles):
    # Current_pos is robot_pos
    distance = math.sqrt((current_pos.x-x)**2 + (current_pos.y-y)**2)
    target_angle = math.degrees(math.atan2((y-current_pos.y),(x-current_pos.x)))
    turn_degrees = (target_angle - current_pos.theta + 540) % 360 - 180
    print(turn_degrees)
    # Turn to face waypoint
    turn(turn_degrees)
    # Move to waypoint
    move_forward(distance)
    particles.update_spread(distance, turn_degrees)

def Navigate_and_update_particles(dest_x, dest_y, robot_pos, particles):
    navigateToWaypoint(dest_x, dest_y, robot_pos, particles)

def fetch_sensor_readings():
    time.sleep(0.5)
    try:
        value1 = BP.get_sensor(BP.PORT_2)
        time.sleep(0.05)
        value2 = BP.get_sensor(BP.PORT_2)
        time.sleep(0.05)
        value3 = BP.get_sensor(BP.PORT_2)
        time.sleep(0.05)
        value4 = BP.get_sensor(BP.PORT_2)
        time.sleep(0.05)
        value5 = BP.get_sensor(BP.PORT_2)
        value = [value1, value2, value3, value4, value5]
        value.sort()
        return (value[2]+2)
    except brickpi3.SensorError as error:
        print(error)
        return None