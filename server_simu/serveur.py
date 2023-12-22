import serial
import requests


SERIALPORT = "/dev/ttyACM0"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():
    ser.port = SERIALPORT
    ser.baudrate = BAUDRATE
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = None
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    print("Starting Up Serial Monitor")
    try:
        ser.open()
    except serial.SerialException:
        print("Serial {} port not available".format(SERIALPORT))
        exit()

def sendUARTMessage(msg):
    ser.write(msg.encode())
    print("Message <" + msg + "> sent to micro:bit.")

def readUARTMessage():
    while ser.inWaiting() > 0:
        message = ser.readline().decode('utf-8').strip()
        message = message.rstrip('\r\n')  # Supprime les caractères de fin de ligne
        print("Received from micro:bit: " + message)

if __name__ == 'main':
    try :
        initUART()
        while(True):
            message_to_send = "id_source:1,id_capteur:5,intensity:6,id_destination:158"
            # response = requests.get("http://localhost:3000/api/sensor/active")
            # if response.status_code == 200:
            #     sendUARTMessage(response.json())


    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        ser.close()