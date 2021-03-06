from time import sleep

from gpiozero import Motor

from robot import Robot
from encoder import QuadratureEncoder
from gps import GPS
from magnetometer import Magnetometer
from controller import PIDController
from manager import RoverManager
#from imageProcessing import ImageProcessing

from sphericalTrigonometry import SphericalPoint

def main():
    dt = 0.01

    LEFT_MOTOR_INPUT = (17, 27)
    RIGHT_MOTOR_INPUT = (5, 6)

    LEFT_ENCODER_INPUT = {'hall_sensor_A': 23, 'hall_sensor_B': 24, 'ticks_per_revolution': 2400}
    RIGHT_ENCODER_INPUT = {'hall_sensor_A': 13, 'hall_sensor_B': 19, 'ticks_per_revolution': 2350}

    left_motor = Motor(LEFT_MOTOR_INPUT[0], LEFT_MOTOR_INPUT[1])
    right_motor = Motor(RIGHT_MOTOR_INPUT[0], RIGHT_MOTOR_INPUT[1])

    left_encoder = QuadratureEncoder(LEFT_ENCODER_INPUT['ticks_per_revolution'], LEFT_ENCODER_INPUT['hall_sensor_A'], LEFT_ENCODER_INPUT['hall_sensor_B'])
    right_encoder = QuadratureEncoder(RIGHT_ENCODER_INPUT['ticks_per_revolution'], RIGHT_ENCODER_INPUT['hall_sensor_A'], RIGHT_ENCODER_INPUT['hall_sensor_B'])

    gps = GPS()
    magnetometer = Magnetometer()

    robot = Robot(left_motor, right_motor, left_encoder, right_encoder, gps, magnetometer)
    controller = PIDController(robot)

    target = SphericalPoint(-12.016592, -77.049883 )

#    target = SphericalPoint(-12.016679333333334,-77.05032666666666)
#    target = SphericalPoint(-12.016824833333333,-77.04993633333333)
#    target = SphericalPoint(-12.016822250210852, -77.04970762346649


    rover_manager = RoverManager(robot, controller, target)

    print(target.toENU(robot.reference))

#    rover_image_manager = ImageProcessing(robot)
#    rover_image_manager.execute()

    epoch = 0
    while(True):
        print("epoch: %d" %epoch)
        gps_enabled = (epoch > 0 and (epoch % 100 == 0))
        rover_manager.execute_with_filter(gps_enabled = gps_enabled)
        epoch += 1

if __name__ == '__main__':
    main()
