from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
import cv2
import os
import time


def main():
	#test focal distance at 20cm
	picam2 = Picamera2()
	mode = picam2.sensor_modes[1]
	config = picam2.create_preview_configuration(main={"size" : (1280, 720), 'format' : 'RGB888'}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=True))
	picam2.align_configuration(config)
	picam2.configure(config)
	lens = picam2.camera_controls['LensPosition']
	picam2.set_controls({"FrameRate" : 50, "AfMode" : controls.AfModeEnum.Manual, "LensPosition" : 20.0})
	#picam2.start_preview(Preview.QT)
	picam2.start()
	cv2.imwrite('focus.jpg', picam2.capture_array())
	'''
	while True:
		if cv2.waitKey(1)==ord('q'):
			break
	picam2.stop_preview()
	picam2.stop()
	'''
	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main()
