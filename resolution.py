from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
import cv2
import time


def main():
	picam2 = Picamera2()
	modes = picam2.sensor_modes
	take_picture(picam2, 'im1.jpg', modes)
	take_picture(picam2, 'im2.jpg', modes)
	
def take_picture(picam2, name, modes):
	qual = get_quality(len(modes))
	config = picam2.create_preview_configuration(main={"size" : (800, 640), "format" : 'RGB888'}, sensor={'output_size' : modes[qual]['size'], 'bit_depth' : modes[qual]['bit_depth']}, transform=Transform(vflip=True))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : 50, "AfMode" : controls.AfModeEnum.Manual, "LensPosition" : 32.0})
	picam2.start()
	img = picam2.capture_array()
	cv2.imwrite(name, img)
	'''
	while True:
		cv2.imshow("image", img)
		if cv2.waitKey(1)==ord('q'):
			cv2.destroyAllWindows()
			break
	picam2.stop()
	'''
	picam2.stop()
	
	
	
def get_quality(numModes):
	#get quality mode
	a = [i for i in range(numModes)]
	while True:
		try:
			mode = int(input(f"Select quality mode {a[0]} through {a[-1]}: "))
			if mode in a:
				return mode
		except:
			print("Invalid choice.")





if __name__ == "__main__":
	main()
