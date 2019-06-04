import math
import py_qmc5883l

class Magnetometer:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L()

    def read(self):
        self.sensor.declination = -1.9312636
#        self.sensor.calibration =  [[1.0235593865542263, -0.0297036331007981, 47.66790112280175], [-0.029703633100797988, 1.0374502883322547, -125.55912192953534], [0.0, 0.0, 1.0]]
        bearing_degrees = self.sensor.get_bearing() - 3.3
        print(bearing_degrees)

        return math.radians(bearing_degrees)


if __name__ == '__main__':
    magnetometer = Magnetometer()
    print(magnetometer.read())
