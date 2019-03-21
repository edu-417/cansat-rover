import math

class Robot():
    def __init__(self, left_motor, right_motor, left_encoder, right_encoder, gps):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.wheel_radius = 0.139
        self.wheel_base_length = 0.212
        self.max_left_wheel_speed = 7.48
        self.max_right_wheel_speed = 7.67
        self.max_speed = 7.48
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.gps = gps
        self.reference = self.gps.read()

    def forward(self, speed = 1):
        self.left_motor.forward(speed)
        self.right_motor.forward(speed)

    def backward(self, speed = 1):
        self.left_motor.backward(speed)
        self.right_motor.backward(speed)

    def update_speed(self, left_wheel_speed, right_wheel_speed):
        left_speed = left_wheel_speed / self.max_left_wheel_speed
        right_speed = right_wheel_speed / self.max_right_wheel_speed
        if left_speed < 0:
            self.left_motor.backward(-left_speed)
        else:
            self.left_motor.forward(left_speed)
        if right_speed < 0:
            self.right_motor.backward(-right_speed)
        else:
            self.right_motor.forward(right_speed)

    def update_speed_normalize(self, left_speed, right_speed):
        self.left_motor.forward(left_speed)
        self.right_motor.forward(right_speed)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
