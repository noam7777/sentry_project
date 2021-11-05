import numpy as np
import matplotlib.pyplot as plt

import cv2, queue, threading, time

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
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

  def read(self):
    return self.q.get()




def detect_faces(cascade, test_image, scaleFactor = 1.1):
    # create a copy of the image to prevent any changes to the original one.
    image_copy = test_image.copy()

    #convert the test image to gray scale as opencv face detector expects gray images
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

    # Applying the haar classifier to detect faces
    faces_rects = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)
    print('Faces found: ', len(faces_rects))

    for (x, y, w, h) in faces_rects:
        image_copy = cv2.rectangle(image_copy, (x+round(w/2-2), y+round(h/2-2)), (x+round(w/2+2), y+round(h/2+2)), (0, 255, 0), 15)

    cv2.imshow("frame", image_copy)
    return faces_rects

if __name__=="__main__":
    haar_cascade_face = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
    
    cap = VideoCapture(0)
    while True:
        #time.sleep(.5)   # simulate time between events
        frame = cap.read()
        rects = detect_faces(haar_cascade_face,frame)
        if len(rects) >= 1:
            print(rects[0])

        if chr(cv2.waitKey(1)&255) == 'q':
            break
    cv2.destroyAllWindows()

