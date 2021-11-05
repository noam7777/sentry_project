import serial
import time
import math
   
class Commander:
    def __init__(self,serial_port_name = '/dev/ttyUSB0', boudrate = 9600,   min_yaw = 0, max_yaw = 180, min_pitch = 80, max_pitch = 178):
        self.min_pitch = min_pitch
        self.max_pitch = max_pitch
        self.min_yaw = min_yaw
        self.max_yaw = max_yaw
        self.ser = serial.Serial(serial_port_name, boudrate, timeout=1)
        self.ser.flush()
        time.sleep(0.2)


    def is_pitch_valid(self, angle):
        if angle%1 != 0 or angle < self.min_pitch  or algle > self.max_pitch : 
            return False
        return True
    def is_yaw_valid(self, angle):
        if angle%1 != 0 or angle < self.min_yaw or algle > self.max_yaw  : 
            return False
        return True

    def angle2string(self, angle):
        order_of_magnitude = math.floor(math.log(angle, 10))
        n_prefix_zeros = 2-order_of_magnitude
        angle_string = ''
        for _ in range(n_prefix_zeros):
            angle_string += '0'
        angle_string += str(angle)
        return angle_string
        
    def send_command(self, cmd_type, yaw, pitch, arm, trigger):
        print('sending command: |type = ' + str(cmd_type)+
              '|yaw = ' + self.angle2string(yaw) +
              '|pitch = ' + self.angle2string(pitch) +
              '|arm = ' + str(arm) +
              '|trigger = ' + str(trigger))
        serial_cmd = f"{str(cmd_type)}-{self.angle2string(yaw)}-{self.angle2string(pitch)}-{str(arm)}-{str(trigger)}\n"
        print("serial command: " + serial_cmd)
#         #ser.write(b"{str(cmd_type)}-{angle2string(yaw)}-{angle2string(pitch)}-{str(arm)}-{str(trigger)}\n")
#         yaw_string = self.angle2string(yaw)
#         print('angle2string(yaw) = ' + yaw_string)
        
        self.ser.write(serial_cmd.encode('UTF-8'))

    
    

if __name__ == '__main__':
    cmdr = Commander()
    while True:
        for yaw in [60,90,120]:
            for pitch in [80,179,178,177,176]:
                cmdr.send_command(1,yaw,pitch,1,1)
                time.sleep(4.0)
