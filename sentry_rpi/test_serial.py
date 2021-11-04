import serial
import time
import math
   
min_servo_pitch = 80
max_servo_pitch = 178

def is_angle_valid(angle):
    if angle%1 != 0 or angle < 0 or algle > 180 : 
        return False
    return True

def angle2string(angle):
    order_of_magnitude = math.floor(math.log(angle, 10))
    n_prefix_zeros = 2-order_of_magnitude
    angle_string = ''
    for _ in range(n_prefix_zeros):
        angle_string += '0'
    angle_string += str(angle)
    return angle_string
    
def send_command(cmd_type, yaw, pitch, arm, trigger):
    print('sending command: |type = ' + str(cmd_type)+
          '|yaw = ' + angle2string(yaw) +
          '|pitch = ' + angle2string(pitch) +
          '|arm = ' + str(arm) +
          '|trigger = ' + str(trigger))
    serial_cmd = f"{str(cmd_type)}-{angle2string(yaw)}-{angle2string(pitch)}-{str(arm)}-{str(trigger)}\n"
    print("serial command: " + serial_cmd)
    #ser.write(b"{str(cmd_type)}-{angle2string(yaw)}-{angle2string(pitch)}-{str(arm)}-{str(trigger)}\n")
    yaw_string = angle2string(yaw)
    print('angle2string(yaw) = ' + yaw_string)
    
    ser.write(serial_cmd.encode('UTF-8'))

    
    

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB1',9600, timeout=1)
    while True:
        for yaw in [60,90,120]:
            for pitch in [80,179,178,177,176]:
                ser.flush()
                send_command(1,yaw,pitch,1,1)
                time.sleep(4.0)
