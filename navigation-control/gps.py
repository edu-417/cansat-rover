from serial import serial

from sphericalTrigonometry import SphericalPoint

class GPS():
    GGA_TYPE = 'GGA'

    def __init__(self, port = "/dev/ttyAMA0"):
        self.port = port

    def parse_nmea_sentence(self, sentence):
        parsed_sentence = {}
        values = sentence.split(',')
        parsed_sentence['type'] = values[0][3:]

        if parsed_sentence['type'] == self.GGA_TYPE:
            latitude = int(values[2][:2]) + float(values[2][2:]) / 60.0
            if values[3] == 'S':
                latitude = -latitude

            longitude = int(values[4][:3]) + float(values[4][3:]) / 60.0
            if values[5] == 'W':
                longitude = -longitude

            parsed_sentence['latitude'] = latitude
            parsed_sentence['longitude'] = longitude

        return parsed_sentence

    def read(self):
        serial = Serial(self.port)
        while True:
            try:
                data = serial.readline()
                sentence = data.decode('utf-8')
                parsed_sentence = self.parse_nmea_sentence(sentence)

                if parsed_sentence['type'] == GGA_TYPE:
                    break
        
        serial.close()

        return SphericalPoint(parsed_sentence['latitude'], parsed_sentence['longitude'])

