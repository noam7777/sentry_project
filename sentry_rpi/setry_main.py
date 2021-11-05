from arduino_commander import Commander
import face_detection
from face_detection import CameraSensor
import cv2
from time import sleep
if __name__ == '__main__':
    haar_cascade_face = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    sensor = CameraSensor(0,haar_cascade_face, frame_width = 640, frame_height = 480, horrizontal_fov = 98.6, vertical_fov = 38.2)
    cmdr = Commander()
    
    while True:
        frame = sensor.read()
        rects = sensor.detect_faces(frame)
        if len(rects) >= 1:
            width_pix = rects[0][2]
            height_pix = rects[0][3]
            x_pix = rects[0][0]+width_pix/2
            y_pix = rects[0][1]+height_pix/2
            cmd_yaw = round(90-(sensor.horrizontal_fov*(x_pix/sensor.frame_width-0.5)))
            cmd_pitch = 170
#             pitch = round(x_pix/sensor.frame_width*sensor.horrizontal_fov)
            cmdr.send_command(1,cmd_yaw,cmd_pitch,1,1)

#             cmd_pitch = rects 

        if chr(cv2.waitKey(1)&255) == 'q':
            break
    cv2.destroyAllWindows()
#         for yaw in [60,90,120]:
#             for pitch in [80,179,178,177,176]:
#                 cmdr.send_command(1,yaw,pitch,1,1)
#                 time.sleep(4.0)