
import paho.mqtt.client as mqtt
import serial

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

def on_publish(client, userdata, result):
    print("Message Published {}".format(result))

mqttServer = '127.0.0.1'
serverPort = 1883
serialPort = 'COM3'
baudrate = 115200

def main():

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.connect(mqttServer, serverPort, 60)

    with serial.Serial(serialPort, baudrate) as ser:
        while( ser.in_waiting > 0):
            ser.readline()
        while( ser.in_waiting == 0):
            continue
        while( ser.in_waiting > 0):
            ser.readline()

        ser.write(b'start')

        count = 0
        while(True):
            if ser.in_waiting == 0:
                continue

            imu_read = ser.readline().decode('utf-8')
            # bme_read = ser.readline().decode('utf-8')
            # uv = float(ser.readline())

            if( count % 20 == 0):
                print(imu_read)
                client.publish('imu/quaternion', payload = imu_read)
                # print(bme_read)
                # bme_read = bme_read.split(',')
                # print(bme_read)
                # humedity = float( bme_read[0] )
                # pressure = float( bme_read[1] ) / 1000
                # altitude = float( bme_read[2] )
                # temperature = float( bme_read[3] ) - 6      
                # client.publish( 'environment/humedity', payload= humedity)
                # client.publish( 'environment/pressure', payload= pressure)
                # client.publish( 'environment/altitude', payload= altitude)
                # client.publish( 'environment/temperature', payload= temperature)
                # client.publish( 'environment/uv', payload= uv)

            count += 1

if __name__ == '__main__':
    main()