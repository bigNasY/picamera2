from picamera2 import Picamera2
import cv2
import rawpy
import numpy as np

picam2 = Picamera2()
print(picam2.sensor_modes)
picam2.configure(picam2.create_preview_configuration(raw={'format' : picam2.sensor_modes[0]['unpacked'], 'size' : picam2.sensor_modes[0]['size']}))
picam2.start()

arr = picam2.capture_array('raw')
picam2.stop()

height, packed_width = arr.shape
unpacked_width = packed_width // 2

raw_16bit = arr.view(np.uint16).reshape(height, unpacked_width)
#print(np.amax(raw_16bit))

img = cv2.cvtColor(raw_16bit, cv2.COLOR_BayerBG2BGR)

img_8bit = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

cv2.imwrite('./rbg_image.jpg', img)


