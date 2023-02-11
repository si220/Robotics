import brickpi3
BP = brickpi3.BrickPi3()
import time

try:
    # restricting speed of motors
    BP.set_motor_limits(BP.PORT_D, 50, 200)
    BP.set_motor_limits(BP.PORT_C, 50, 200)
    
    for i in range(4):
        for j in range(4):

            # reset encoder position in between each movement
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
            BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

            # drive 10cm in a straight line
            BP.set_motor_position(BP.PORT_D, 166)
            BP.set_motor_position(BP.PORT_C, 166)

            time.sleep(0.5)
        
            # check if motor velocity = 0
            while BP.get_motor_status(BP.PORT_D)[3] != 0:
                pass

        # reset encoder position in between each movement
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))

        # turn 90 degrees
        BP.set_motor_position(BP.PORT_D, 193) #780 is 360 degree turn on paper above carpet, 749 is 360 turn on wood table, 805 is on carpet
        BP.set_motor_position(BP.PORT_C, -193)

        time.sleep(0.5)
        
        # check if motor velocity = 0
        while BP.get_motor_status(BP.PORT_D)[3] != 0:
            pass

except KeyboardInterrupt:
    BP.reset_all()
