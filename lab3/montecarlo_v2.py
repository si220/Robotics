import time
import montecarlo_classes as mc

# global canvas we are going to draw on
canvas = mc.Canvas()
mymap = mc.Map(canvas)

# Definitions of walls
mymap.add_wall((0,0,0,168))        # a: O to A
mymap.add_wall((0,168,84,168))     # b: A to B
mymap.add_wall((84,126,84,210))    # c: C to D
mymap.add_wall((84,210,168,210))   # d: D to E
mymap.add_wall((168,210,168,84))   # e: E to F
mymap.add_wall((168,84,210,84));   # f: F to G
mymap.add_wall((210,84,210,0))     # g: G to H
mymap.add_wall((210,0,0,0))        # h: H to O
mymap.draw()

# initialize particle count
num_particles = 100

waypoints = [(84, 30), (104,30),(124,30),(150,30), (180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]

initial_robot_position = (waypoints[0][0], waypoints[0][1], 0)
# initialize x, y, and theta for each particle
particles = mc.Particles(canvas, n_particles=100, initial_pos = initial_robot_position)
robot_pos = mc.Robot_position(initial_pos = initial_robot_position)
print(robot_pos.x, robot_pos.y, robot_pos.theta)

for i in range(1, len(waypoints)):
    particles.draw()
    time.sleep(1)
    mc.Navigate_and_update_particles(waypoints[i][0], waypoints[i][1], robot_pos, particles)
    reading = mc.fetch_sensor_readings()
    particles.update_weights(mymap, reading)
    print("Parents",particles.data)
    print("Weights:",particles.weights)
    particles.resample()
    print("Babies:",particles.data)
    print("Weights:",particles.weights)
    robot_pos.update(particles)
    print(f"Current x: {robot_pos.x}, Current y: {robot_pos.y}, Current theta: {robot_pos.theta}")
