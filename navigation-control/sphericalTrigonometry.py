import math

def degreesToRadians(degrees):
    return math.pi / 180

class SphericalPoint():
    def __init__(self, latitude = 0 , longitude = 0):
            self.latitude = latitude
            self.longitude = longitude

    def bearingTo(self, destination):
        phi1 = degreesToRadians(self.latitude)
        phi2 = degreesToRadians(destination.latitude)
        delta_lambda = degreesToRadians(destination.longitude - self.longitude)

        x = math.cos( phi1 ) * math.sin( phi2 ) - math.sin( phi1 ) * math.cos( phi2 ) * math.cos( delta_lambda )
        y = math.sin( delta_lambda ) * math.cos( phi2 )

        theta = math.atan2(y, x)

        return theta    