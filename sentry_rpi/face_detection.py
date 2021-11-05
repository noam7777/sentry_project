import numpy as np
import matplotlib.pyplot as plt
import cv2, queue, threading, time

# bufferless VideoCapture
class CameraSensor:
    def __init__(self, name, cascade, frame_width = 640, frame_height = 480, horrizontal_fov = 49.6, vertical_fov = 38.2):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.horrizontal_fov = horrizontal_fov
        self.vertical_fov = vertical_fov
        self.cascade = cascade
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

#   # read frames as soon as they are available, keeping only most recent one
#   def _reader(self):
#     while True:
#       ret, frame = self.cap.read()
#       if not ret:
#         break
#       if not self.q.empty():
#         try:
#           self.q.get_nowait()   # discard previous (unprocessed) frame
#         except queue.Empty:
#           pass
#       self.q.put(frame)


    def read(self):
        return self.q.get()



    def detect_faces(self, image, scaleFactor = 1.1):
        # create a copy of the image to prevent any changes to the original one.
        image_copy = image.copy()

        #convert the test image to gray scale as opencv face detector expects gray images
        gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

        # Applying the haar classifier to detect faces
        faces_rects = self.cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)
        print('Faces found: ', len(faces_rects))
        face_location = []
        for (x, y, w, h) in faces_rects:
            image_copy = cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 4)
        cv2.imshow("frame", image_copy)
        
        return faces_rects

if __name__=="__main__":
    haar_cascade_face = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    
    sensor = CameraSensor(0,haar_cascade_face)
    while True:
        #time.sleep(.5)   # simulate time between events
        frame = sensor.read()
        rects = sensor.detect_faces(frame)
        if len(rects) >= 1:
            print(rects[0])

        if chr(cv2.waitKey(1)&255) == 'q':
            break
    cv2.destroyAllWindows()

