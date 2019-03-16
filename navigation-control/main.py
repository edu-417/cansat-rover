from time import sleep

from gpiozero import Motor

from robot import Robot
from encoder import QuadratureEncoder
from gps import GPS
from controller import PIDController
from manager import RoverManager

def main():
    dt = 0.1

    LEFT_MOTOR_INPUT = (17, 27)
    RIGHT_MOTOR_INPUT = (5, 6)
     
    LEFT_ENCODER_INPUT = {'hall_sensor_A': 23, 'hall_sensor_B': 24, 'ticks_per_revolution': 2400}
    RIGHT_ENCODER_INPUT = {'hall_sensor_A': 13, 'hall_sensor_B': 19, 'ticks_per_revolution': 2350}

    left_motor = Motor(LEFT_MOTOR_INPUT[0], LEFT_MOTOR_INPUT[1])
    right_motor = Motor(RIGHT_MOTOR_INPUT[0], RIGHT_MOTOR_INPUT[1])

    left_encoder = QuadratureEncoder(LEFT_ENCODER_INPUT['ticks_per_revolution'], LEFT_ENCODER_INPUT['hall_sensor_A'], LEFT_ENCODER_INPUT['hall_sensor_B'])
    right_encoder = QuadratureEncoder(RIGHT_ENCODER_INPUT['ticks_per_revolution'], RIGHT_ENCODER_INPUT['hall_sensor_A'], RIGHT_ENCODER_INPUT['hall_sensor_B'])

    gps = GPS()

    robot = Robot(left_motor, right_motor, left_encoder, right_encoder, gps)
    controller = PIDController(robot)

    target = {'x': 0 , 'y': 1}

    rover_manager = RoverManager(robot, controller, target)

    while(True):
        rover_manager.execute_with_gps()
        print(robot.left_encoder.counter)
        print(robot.right_encoder.counter)
        sleep(dt)

if __name__ == '__main__':
    main()
