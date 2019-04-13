import numpy as np

class KalmanFilter():
    def __init__(self, robot):
        self.robot = robot

        self.H = np.array([
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0]
        ])

        self.P = np.array([
            [1000, 0, 0, 0, 0],
            [0, 1000, 0, 0, 0],
            [0, 0, 100, 0, 0],
            [0, 0, 0, 1000, 0],
            [0, 0, 0, 0, 1000]
        ])

        self.Q = np.identity(5)

        self.R = np.array([
            [100, 0, 0],
            [0, 100, 0],
            [0, 0, 25]
        ])

    def predict(self, x, dt = 0.01):

        speed = self.robot.speed
        theta = self.robot.theta

        F = np.array([
            [1, 0, -speed * dt * np.sin(theta), dt * np.cos(theta), 0],
            [0, 1,  speed * dt * np.cos(theta), dt * np.sin(theta), 0],
            [0, 0,                           1,                  0, dt],
            [0, 0,                           0,                  1, 0],
            [0, 0,                           0,                  0, 1]
        ])
        #x = f(x, u)
        self.P = F @ self.P @ F.transponse() + self.Q

        return x

    def update(self, z):

        I = np.identity(5)

        y = z - self.H @ x
        S = self.H @ self.P @ self.H.transponse() + self.R
        K = self.P @ self.H.transponse() * np.linalg.inverse(self.S)

        x = x + K @ y
        self.P = (I - K @ self.H) @ self.P

        return x


    def filter(self, x, z):

        x = self.update(z)

        x = self.predict(x)

        return x


