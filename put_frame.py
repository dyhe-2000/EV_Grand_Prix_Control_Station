import cv2
import time

while True:
    vidcap = cv2.VideoCapture('clip.mp4')
    success,image = vidcap.read()
    count = 0
    while success:
      # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file  
      cv2.imwrite("frame.jpg", image)
      time.sleep(1)
      success,image = vidcap.read()
      print('Read a new frame: ', success)
      count += 1