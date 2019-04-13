import math
from filter import KalmanFilter

class RoverManager():
    def __init__(self, robot, controller, target):
        self.robot = robot
        self.controller = controller
        self.previous_left_ticks = 0
        self.previous_right_ticks = 0
        self.target = target
        self.filter = KalmanFilter()
    
    def distance_per_ticks(self, ticks, wheel_radius, ticks_per_revolution):
        return 2 * math.pi * wheel_radius / ticks_per_revolution * ticks

    def update_odometry(self):

        left_encoder_ticks = self.robot.left_encoder.counter
        right_encoder_ticks = -self.robot.right_encoder.counter
        left_wheel_distance = self.distance_per_ticks(left_encoder_ticks - self.previous_left_ticks, self.robot.wheel_radius, self.robot.left_encoder.ticks_per_revolution)
        right_wheel_distance = self.distance_per_ticks(right_encoder_ticks - self.previous_right_ticks, self.robot.wheel_radius, self.robot.right_encoder.ticks_per_revolution)

        distance = (left_wheel_distance + right_wheel_distance ) / 2
        phi = (right_wheel_distance - left_wheel_distance) / self.robot.wheel_base_length

        dx = distance * math.cos(self.robot.theta)
        dy = distance * math.sin(self.robot.theta)
        dtheta = phi

        self.robot.x += dx
        self.robot.y += dy
        self.robot.theta += dtheta

        self.previous_left_ticks = left_encoder_ticks
        self.previous_right_ticks = right_encoder_ticks

    def unicycle_to_differential(self, v, w):
        left_speed = (2 * v - w * self.robot.wheel_base_length) / (2 * self.robot.wheel_radius)
        right_speed = (2 * v + w * self.robot.wheel_base_length) / (2 * self.robot.wheel_radius)

        return left_speed, right_speed

    def execute_with_gps(self):

        v, w = self.controller.control_with_gps(self.target)

        max_w = 2 * self.robot.wheel_radius * min(self.robot.max_left_wheel_speed, self.robot.max_right_wheel_speed) / self.robot.wheel_base_length
        w = max(min(w, max_w), -max_w)

        print("w: %f", w)

        left_speed, right_speed = self.unicycle_to_differential(v, w)

        print("vl: %f, vr: %f" %(left_speed, right_speed))

        if( max(left_speed, right_speed) > self.robot.max_speed ):
            if left_speed > right_speed:
                left_speed = self.robot.max_speed
                right_speed = w * self.robot.wheel_base_length / self.robot.wheel_radius  + left_speed
            else:
                right_speed = self.robot.max_speed
                left_speed = right_speed - w * self.robot.wheel_base_length / self.robot.wheel_radius

        elif( min(left_speed, right_speed) < -self.robot.max_speed ):
            if left_speed < right_speed:
                left_speed = -self.robot.max_speed
                right_speed = w * self.robot.wheel_base_length / self.robot.wheel_radius  + left_speed
            else:
                right_speed = -self.robot.max_speed
                left_speed = right_speed - w * self.robot.wheel_base_length / self.robot.wheel_radius


        print("vl: %f, vr: %f" %(left_speed, right_speed))

        self.robot.update_speed(left_speed, right_speed)

        self.update_odometry()

    def ensure_wheel_speeds(self, left_speed, right_speed, w):
        if( max(left_speed, right_speed) > self.robot.max_speed ):
            if left_speed > right_speed:
                left_speed = self.robot.max_speed
                right_speed = w * self.robot.wheel_base_length / self.robot.wheel_radius  + left_speed
            else:
                right_speed = self.robot.max_speed
                left_speed = right_speed - w * self.robot.wheel_base_length / self.robot.wheel_radius

        elif( min(left_speed, right_speed) < -self.robot.max_speed ):
            if left_speed < right_speed:
                left_speed = -self.robot.max_speed
                right_speed = w * self.robot.wheel_base_length / self.robot.wheel_radius  + left_speed
            else:
                right_speed = -self.robot.max_speed
                left_speed = right_speed - w * self.robot.wheel_base_length / self.robot.wheel_radius

        return left_speed, right_speed

    def execute(self):
        v, w = self.controller.control(self.target)

        max_w = 2 * self.robot.wheel_radius * min(self.robot.max_left_wheel_speed, self.robot.max_right_wheel_speed) / self.robot.wheel_base_length
        w = max(min(w, max_w), -max_w)

        print("w: %f", w)

        left_speed, right_speed = self.unicycle_to_differential(v, w)

        print("vl: %f, vr: %f" %(left_speed, right_speed))

        left_speed, right_speed = self.ensure_wheel_speeds(left_speed, right_speed, w)

        print("vl: %f, vr: %f" %(left_speed, right_speed))

        self.robot.update_speed(left_vspeed, right_speed)
        self.robot.speed = v
        self.robot.w = w

        self.update_odometry()


    def execute_with_filter(self):
        v, w = self.controller.control(self.target)

        max_w = 2 * self.robot.wheel_radius * min(self.robot.max_left_wheel_speed, self.robot.max_right_wheel_speed) / self.robot.wheel_base_length
        w = max(min(w, max_w), -max_w)

        print("w: %f", w)

        left_speed, right_speed = self.unicycle_to_differential(v, w)

        print("vl: %f, vr: %f" %(left_speed, right_speed))

        left_speed, right_speed = self.ensure_wheel_speeds(left_speed, right_speed, w)

        print("vl: %f, vr: %f" %(left_speed, right_speed))

        self.robot.update_speed(left_speed, right_speed)

        time.sleep(dt)


        state = self.filter.predict(robot.get_state())
        robot.set_state(state)

        state = self.filter.update(robot.get_state(), Z )
        robot.set_state(state)


