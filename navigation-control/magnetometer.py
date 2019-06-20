import math
import py_qmc5883l
import pickle

class Magnetometer:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L()

    def load_model(self):
        with open('magnetometer_calibration.pickle', 'rb') as handle:
            model = pickle.load(handle)
            return model

        return None

    def read(self):
        self.sensor.declination = -1.9312636
#        self.sensor.calibration =  [[1.0235593865542263, -0.0297036331007981, 47.66790112280175], [-0.029703633100797988, 1.0374502883322547, -125.55912192953534], [0.0, 0.0, 1.0]]
        bearing_degrees = self.sensor.get_bearing() - 3.3
        print(bearing_degrees)
        

        model = self.load_model()

        if(model is None):
            print('Can not load model to calibrate.')
            return math.radians(bearing_degrees)

        calibrated_bearing_degrees = model.predict(np.array(bearing_degrees).reshape(1, -1))[0]

        return math.radians(calibrated_bearing_degrees)


if __name__ == '__main__':
    magnetometer = Magnetometer()
    print(magnetometer.read())
