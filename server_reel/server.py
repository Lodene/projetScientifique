import serial
import requests

SERIALPORT = "/dev/ttyACM0"  # Assurez-vous que le port série est correct
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
    except serial.SerialException as e:
        print("Serial {} port not available".format(SERIALPORT))
        print("Error opening serial port: {}".format(e))
        exit()

def readUARTMessage():
    while(True):
        if ser.in_waiting > 0:
            print(ser.readline().strip())

def getApi(api_url):
    try:
        response = requests.get("http://localhost:3000" + api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    try:
        # initUART()
        id_source_value = None
        id_capteur_value = None
        intensity_value = None
        id_destination_value = None

        while True:
            sensors = getApi("/api/sensor")
            data = readUARTMessage()
            if data is not None and data != "":
                print(data)
                parts = data.split(',')
                for part in parts:
                    key_value = part.split(':')
                    if len(key_value) == 2:
                        key, value = key_value
                        if key == 'id_source':
                            id_source_value = int(value)
                        elif key == 'id_capteur':
                            id_capteur_value = int(value)
                        elif key == 'intensity':
                            intensity_value = int(value)
                        elif key == 'id_destination':
                            id_destination_value = int(value)
                #print("Received: id_source:", id_source_value, ", id_capteur:", id_capteur_value, ", intensity:", intensity_value, ", id_destination:", id_destination_value)
                capteur = getApi("/api/sensor/", id_capteur_value)
                if capteur is not None and capteur != "": #si on trouve le capteur dans la bdd
                    #alors on réupère ses coordonnées et on lance la fonction get_capteurs_proches
                    #on regarde si ces capteurs ont une intensité > 0
                    #si c'est le cas, alors on associe le capteur au feu où le capteur est déjà associé
                    #sinon on crée un nouveau feu
                    
                    


    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        ser.close()