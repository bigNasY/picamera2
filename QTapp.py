from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from picamera2.previews.qt import QGlPicamera2
import cv2
import time


cur_task = ''
t_end = 0
exposure_time = 50000
scale = 1.05
picam2 = Picamera2()
target = 0
cur_task = ''
min_exp, max_exp, def_exp = picam2.camera_controls['ExposureTime']
exposure_time = (max_exp + min_exp) // 2
scale = 1.05
frame_rate = 50
lens_pos = 32
mode = picam2.sensor_modes[0]
print(mode)
config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
picam2.align_configuration(config)
picam2.configure(config)
picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, 'LensPosition' : lens_pos})


def on_button1_clicked():
	button1.setEnabled(False)
	global scale
	scale=0.95
	global cur_task 
	cur_task = 'zoom'
	picam2.capture_metadata(signal_function=qpicamera2.signal_done)
	


def on_button2_clicked():
	button2.setEnabled(False)
	global scale
	scale = 1.05
	global cur_task 
	cur_task = 'zoom'
	picam2.capture_metadata(signal_function=qpicamera2.signal_done)
	


def on_button3_clicked():
	button3.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[2]
	print(mode)
	config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	button4.setEnabled(True)
	button5.setEnabled(True)
	
	
def on_button4_clicked():
	button4.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[0]
	config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	button3.setEnabled(True)
	button5.setEnabled(True)

	
def on_button5_clicked():
	button5.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[1]
	print(mode)
	config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	button3.setEnabled(True)
	button4.setEnabled(True)
	
	
def on_button6_clicked():
	global cur_task
	cur_task = 'fr'
	t_start = time.time()
	
	cfg = picam2.create_still_configuration()


	
	picam2.switch_mode_and_capture_file(cfg, 'img.jpg', signal_function=qpicamera2.signal_done)
	t_end = time.time()
	
	picam2.stop()
	config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, 'LensPosition' : lens_pos}) 
	picam2.start()
	t = t_end - t_start
	print(t_end)
	print(f'Time to capture one image: {t}')
	


def zoom_done(job):
	global cur_task
	result = picam2.wait(job)
	if cur_task == 'zoom':
		full_res = picam2.camera_properties['PixelArraySize']
		size = result['ScalerCrop'][2:]
		newSize = [int(s * scale) for s in size]
		offset = [(r - s) // 2 for r, s in zip(full_res, newSize)]
		picam2.set_controls({'ScalerCrop' : offset+newSize})
		button1.setEnabled(True)
		button2.setEnabled(True)
	
	

def value_changed(i):
	try:
		e = int(i)
		if(e >= 0 and e <= 66):
			global exposure_time
			exposure_time = e *1000
			picam2.set_controls({"ExposureTime" : e *1000})
			
	except:
		pass


def text_changed(val):
	try:
		if int(val) >= 1 and int(val) <= 32: 
			global lens_pos
			lens_pos = int(val)
			picam2.set_controls({'LensPosition' : int(val)})
	except:
		pass


def frame_text_changed(val):
	try:
		f = int(val)
		if(f > 0):
			global frame_rate
			frame_rate = f
			picam2.set_controls({'FrameRate' : f})	
	except:
		pass
		

app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=1280, height=720, keep_ar=False)

button1 = QPushButton("Click to zoom in")
window = QWidget()
qpicamera2.done_signal.connect(zoom_done)
button1.clicked.connect(on_button1_clicked)


button2 = QPushButton("Click to zoom out")
button2.clicked.connect(on_button2_clicked)

button3 = QPushButton("2592p")
button3.clicked.connect(on_button3_clicked)

button4 = QPushButton("864p")
button4.clicked.connect(on_button4_clicked)
button4.setEnabled(False)

button5 = QPushButton("1296p")
button5.clicked.connect(on_button5_clicked)

button6 = QPushButton("Test Frame Rate")
button6.clicked.connect(on_button6_clicked)

expTimeSlider = QLineEdit()
expTimeSlider.setMaxLength(4)
expTimeSlider.textEdited.connect(value_changed)
expTimeSlider.setPlaceholderText(f'Exposure Time ({min_exp // 1000} to {max_exp // 1000} ms.)')



focalDistEdit = QLineEdit()
focalDistEdit.setMaxLength(2)
focalDistEdit.setPlaceholderText('Enter focal distance (1 to 32 cm)')
focalDistEdit.textEdited.connect(text_changed)

frameEdit = QLineEdit()
frameEdit.setMaxLength(3)
frameEdit.setPlaceholderText('Enter Frame Rate')
frameEdit.textEdited.connect(frame_text_changed)

label2 = QLabel()
label2.setText('Frame Rate Test')



layout = QHBoxLayout()


layout_v3 = QHBoxLayout()
layout_v3.addWidget(button4)
layout_v3.addWidget(button5)
layout_v3.addWidget(button3)

layout_v4 = QHBoxLayout()
layout_v4.addWidget(frameEdit)
layout_v4.addWidget(button6)

layout_v = QVBoxLayout()
layout_v.setSpacing(10)
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button1)
layout_v.addWidget(button2)
layout_v.addLayout(layout_v3)
layout_v.addWidget(focalDistEdit)
layout_v.addWidget(expTimeSlider)
layout_v.addLayout(layout_v4)





layout.addLayout(layout_v)



qpicamera2.setWindowTitle("sigma")
window.setLayout(layout)
window.resize(800, 800)
picam2.start()
window.show()
app.exec()


