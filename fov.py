from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform
import cv2
import time


def main():
	picam2 = Picamera2()
	mode = picam2.sensor_modes[0]
	config = picam2.create_preview_configuration(main={"size" : (1280, 720), "format" : 'RGB888'}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=True))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : 50})
	picam2.start()
	#cv2.imwrite('full.jpg', picam2.capture_array())
	#print(picam2.camera_properties['PixelArraySize'])
	#print(picam2.capture_metadata()['ScalerCrop'])
	
	change_fov(picam2, name="zoom.jpg", scale=0.6)
	#half_fov(picam2)
	picam2.stop()
	

def change_fov(picam2, name='test.jpg', scale=1):
	#this changes fov only in a zoom/pan manner.
	#It is possible to select portions of the image (e.g. just the top half), but that image is then scaled to a wonky aspect ratio.
	full_res = picam2.camera_properties['PixelArraySize']
	size = picam2.capture_metadata()['ScalerCrop'][2:]
	
	newSize = [int(s * scale) for s in size]
	offset = [(r - s) // 2 for r, s in zip(full_res, newSize)]
	picam2.set_controls({"ScalerCrop": offset + newSize})
	time.sleep(2)
	picam2.capture_metadata()
	img = picam2.capture_array()
	cv2.imwrite(name,img)
	#show_img(img)
	
	
def half_fov(picam2):
	#example of the aforementioned halfing of the camera's vertical fov while keeping horizontal untouched.
	full_res = picam2.camera_properties['PixelArraySize']
	size = picam2.capture_metadata()['ScalerCrop'][2:]
	
	newSize = (size[0], size[1] // 2)
	offset = (size[0], size[1] // 4)
	picam2.set_controls({"ScalerCrop": offset + newSize})
	time.sleep(2)
	picam2.capture_metadata()
	img = picam2.capture_array()
	cv2.imwrite('half.jpg', img)
	#show_img(img)
	


def show_img(img):
	while True:
		cv2.imshow("image", img)
		if cv2.waitKey(1)==ord('q'):
			cv2.destroyAllWindows()
			break




if __name__ == "__main__":
	main()
	
