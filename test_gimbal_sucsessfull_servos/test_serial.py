import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB1',9600, timeout=1)
    ser.flush()
    
    while True:
        ser.write(b"1-131-113-1-1\n")
        time.sleep(1)