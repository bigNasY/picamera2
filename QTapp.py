from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from picamera2.previews.qt import QGlPicamera2
from picamera2.outputs import FileOutput
import cv2
import time
import datetime
import sys
import os

t_start = 0
t_end = 0
recording = False
file_name = ''
cur_task = ''
app = QApplication([])
capture_time = 1
scale = 1.05
picam2 = Picamera2()
target = 0
cur_task = ''
min_exp, max_exp, def_exp = picam2.camera_controls['ExposureTime']
exposure_time = (max_exp + min_exp) // 2
scale = 1.05
frame_rate = 30
lens_pos = 32
x1 = 0;
x2 = 4608;
y1 = 0;
y2 = 2592;
mode = picam2.sensor_modes[0]
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
	global mode
	label.setText('4608 x 2592')
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
	global mode
	label.setText('1536 x 864')
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
	global mode
	label.setText('2304 x 1296')
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
	picam2.capture_file(f'/home/bob/images/img{str(time.time())[-4:]}.jpg', signal_function=qpicamera2.signal_done)
	
	
def on_button7_clicked():
	
	
	'''
	for _ in range(int(capture_time*frame_rate)):
		picam2.capture_file(f'/home/bob/images/img{str(time.time())[-4:]}.jpg', signal_function=qpicamera2.signal_done)
	'''
	global recording
	global file_name
	global t_start
	global t_end
	if not recording:
		encoder = H264Encoder(10000000)
		file_name = str(time.time())[-4:]
		output = FileOutput(f'test{file_name}.h264')
		picam2.start_encoder(encoder, output)
		t_start = time.time()
		button7.setText('stop recording')
		recording = True
	else:
		picam2.stop_encoder()
		t_end = time.time()
		button7.setText('start recording')
		recording = False
		path = os.getcwd()
		vid = cv2.VideoCapture(f'{path}/test{file_name}.h264')
		count = 0
		success = 1
		while success:
			try:
				success, image = vid.read()
				#print(image)
				cv2.imwrite(f'/home/bob/images/img{str(time.time())[-4:]}.jpg', image)
				count += 1
			except:
				break
		fps = count/(t_end - t_start)
		print(count)
		print(f' Video FPS: {fps}')
	
def on_x1_changed(val):
	global x1
	try:
		x = int(val)
		if(x >= 0 and x <= 4608):
			x1 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
		
def on_x2_changed(val):
	global x2
	try:
		x = int(val)
		if(x >= 0 and x <= 4608):
			x2 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
	
	
def on_y1_changed(val):
	global y1
	try:
		x = int(val)
		if(x >= 0 and x <= 2592):
			y1 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
		
def on_y2_changed(val):
	global y2
	try:
		x = int(val)
		if(x >= 0 and x <= 2592):
			y2 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
	

def on_cropper_clicked():
	global cur_task
	cur_task = 'crop'
	try:
		full_res = picam2.camera_properties['PixelArraySize']
		offset = [x1, y1]
		size = [x2-x1, y2-y1]
		picam2.set_controls({'ScalerCrop' : offset+size})
		label.setText(f'{size[0]} x {size[1]}')
	except:
		pass
		
def on_cropper2_clicked():
	global cur_task
	cur_task = 'cropp'
	picam2.capture_array('main', signal_function=qpicamera2.signal_done)


def zoom_done(job):
	global cur_task
	result = picam2.wait(job)
	if cur_task == 'zoom':
		full_res = picam2.camera_properties['PixelArraySize']
		size = result['ScalerCrop'][2:]
		print('SIZE: ' + str(size))
		newSize = [int(s * scale) for s in size]
		offset = [(r - s) // 2 for r, s in zip(full_res, newSize)]
		picam2.set_controls({'ScalerCrop' : offset+newSize})
		button1.setEnabled(True)
		button2.setEnabled(True)
		label.setText(f'{newSize[0]} x {newSize[1]}')
	if cur_task == 'cropp':
		pass
	
	

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
		if int(val) >= 0 and int(val) <= 32: 
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
		

		


qpicamera2 = QGlPicamera2(picam2, width=1280, height=720, keep_ar=True)

button1 = QPushButton("Click to zoom in")
window = QWidget()
qpicamera2.done_signal.connect(zoom_done)
button1.clicked.connect(on_button1_clicked)


button2 = QPushButton("Click to zoom out")
button2.clicked.connect(on_button2_clicked)

button3 = QPushButton("11.94 Mp")
button3.clicked.connect(on_button3_clicked)

button4 = QPushButton("1.33 Mp")
button4.clicked.connect(on_button4_clicked)
button4.setEnabled(False)

button5 = QPushButton("2.99 Mp")
button5.clicked.connect(on_button5_clicked)

button6 = QPushButton("Capture One Image")
button6.clicked.connect(on_button6_clicked)

button7 = QPushButton('Start continuous image capture')
button7.clicked.connect(on_button7_clicked)





expTimeSlider = QLineEdit()
expTimeSlider.setMaxLength(4)
expTimeSlider.textEdited.connect(value_changed)
expTimeSlider.setPlaceholderText(f'Exposure Time ({min_exp // 1000} to {max_exp // 1000} ms.)')



focalDistEdit = QLineEdit()
focalDistEdit.setMaxLength(2)
focalDistEdit.setPlaceholderText('Enter focal distance (0 to 32 cm)')
focalDistEdit.textEdited.connect(text_changed)

frameEdit = QLineEdit()
frameEdit.setMaxLength(3)
frameEdit.setPlaceholderText('Enter Frame Rate')
frameEdit.textEdited.connect(frame_text_changed)

x1edit = QLineEdit()
x1edit.setMaxLength(4)
x1edit.setPlaceholderText('X1 coordinate')
x1edit.textEdited.connect(on_x1_changed)

x2edit = QLineEdit()
x2edit.setMaxLength(4)
x2edit.setPlaceholderText('X2 coordinate')
x2edit.textEdited.connect(on_x2_changed)

y1edit = QLineEdit()
y1edit.setMaxLength(4)
y1edit.setPlaceholderText('Y1 coordinate')
y1edit.textEdited.connect(on_y1_changed)

y2edit = QLineEdit()
y2edit.setMaxLength(4)
y2edit.setPlaceholderText('Y2 coordinate')
y2edit.textEdited.connect(on_y2_changed)

cropper = QPushButton('Crop Image')
cropper.clicked.connect(on_cropper_clicked)

cropper2 = QPushButton('Crop Image 2')
cropper2.clicked.connect(on_cropper2_clicked)

label = QLabel('1532 x 864')
label.setFixedSize(300, 20)


layout = QHBoxLayout()

layout_h = QHBoxLayout()
layout_h.addWidget(button7)

layout_h2 = QHBoxLayout()
layout_h2.addWidget(x1edit)
layout_h2.addWidget(x2edit)
layout_h2.addWidget(y1edit)
layout_h2.addWidget(y2edit)
layout_h2.addWidget(cropper)




layout_v3 = QHBoxLayout()
layout_v3.addWidget(button4)
layout_v3.addWidget(button5)
layout_v3.addWidget(button3)

layout_v4 = QHBoxLayout()
layout_v4.addWidget(frameEdit)
layout_v4.addWidget(button6)

layout_v = QVBoxLayout()
layout_v.setSpacing(10)
layout_v.addWidget(label)
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button1)
layout_v.addWidget(button2)
layout_v.addLayout(layout_v3)
layout_v.addWidget(focalDistEdit)
layout_v.addWidget(expTimeSlider)
layout_v.addLayout(layout_v4)
layout.addLayout(layout_v)
layout_v.addLayout(layout_h)
layout_v.addLayout(layout_h2)



qpicamera2.setWindowTitle("sigma")
window.setLayout(layout)
window.resize(800, 800)
picam2.start()
window.show()
app.exec()


