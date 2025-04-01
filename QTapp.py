from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
from PyQt5 import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont
from picamera2.previews.qt import QGlPicamera2
from picamera2.outputs import FileOutput
import cv2
import time
import datetime
import sys
import os
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
import math

picam2 = Picamera2()
t_start = 0
t_end = 0
recording = False
file_name = 'img'
cur_task = ''
dir_name = 'images'
path = ''
app = QApplication([])
overlay = np.zeros((720, 1280, 4), dtype=np.uint8)
capture_time = 1
scale = 1.05
target = 0
cur_task = ''
print(picam2.camera_controls['ExposureTime'])
min_exp, max_exp, def_exp = picam2.camera_controls['ExposureTime']
exposure_time = (max_exp + min_exp) // 2
scale = 1.05
frame_rate = 30
lens_pos = 32
print(picam2.camera_controls['LensPosition'])
x1 = 0
x2 = 4608
y1 = 0
y2 = 2592
mode = picam2.sensor_modes[0]
actual_size = [i for i in mode['size']]
config = picam2.create_preview_configuration(main={'size' : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
picam2.align_configuration(config)
picam2.configure(config)
picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, 'LensPosition' : lens_pos})



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self):
        change_config(picam2.create_still_configuration(main={'size' : actual_size}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False)))
       
        t_end = time.time() + 5.0
        while time.time() <= t_end:
            picam2.capture_file(f'{path}/{file_name + str(time.time())[-4:]}.jpg')
         
        change_config(picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False)))   
        
        self.finished.emit()

thread = QThread()
worker = Worker()
def change_config(cfg):
    picam2.stop()
    picam2.configure(cfg)
    picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
    picam2.start()



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
	global actual_size
	global overlay
	#overlay = np.zeros((2592, 4608, 4), dtype=np.uint8)
	#qpicamera2.set_overlay(overlay)
	actual_size = [4608, 2592]
	label.setText('4608 x 2592')
	button3.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[2]
	print(mode)
	config = picam2.create_preview_configuration(main={'size' : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	
	button4.setEnabled(True)
	button5.setEnabled(True)
	
	
def on_button4_clicked():
	global mode
	global actual_size
	global overlay
	#overlay = np.zeros((864, 1536, 4), dtype=np.uint8)
	actual_size = [1536, 864]
	label.setText('1536 x 864')
	button4.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[0]
	config = picam2.create_preview_configuration(main={'size' : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	#qpicamera2.set_overlay(overlay)
	button3.setEnabled(True)
	button5.setEnabled(True)

	
	
	
def on_button5_clicked():
	global mode
	global actual_size
	global overlay
	#x1, y1, x2, y2 = 0, 0, 0, 0
	#overlay = np.zeros((1296, 2304, 4), dtype=np.uint8)
	#qpicamera2.set_overlay(overlay)
	actual_size = [2304, 1296]
	label.setText('2304 x 1296')
	button5.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[1]
	print(mode)
	config = picam2.create_preview_configuration(main={'size' : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	qpicamera2.set_overlay(overlay)
	button3.setEnabled(True)
	button4.setEnabled(True)
	
	
def on_button6_clicked():
	global cur_task
	cur_task = 'fr'
	cfg = picam2.create_still_configuration(main={'size' : actual_size}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
	
	picam2.switch_mode_and_capture_file(cfg, f'/home/bob/images/img{str(time.time())[-4:]}.jpg', signal_function=qpicamera2.signal_done)
	
	
def on_button7_clicked():
	global path
	cwd = os.getcwd()
	path = f'{cwd}/{dir_name}'
	os.mkdir(path)
	worker.moveToThread(thread)
	thread.started.connect(worker.run)
	worker.finished.connect(thread.quit)
	thread.start()

	
def on_x1_changed(val):
	global x1
	ratio = 1280 / actual_size[0] 
	print(ratio)
	overlay[:1280, math.floor(x1*ratio)] = (0, 0, 0, 0)
	try:
		
		x = int(val)
		print(x)
		if(x >= 0 and x <= actual_size[0]):
			x1 = x
			overlay[:1280, math.floor(x*ratio)] = (0, 0, 0, 64)
			qpicamera2.set_overlay(overlay)
			print('hello')
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
		
def on_x2_changed(val):
	global x2
	try:
		x = int(val)
		if(x >= x1 and x <= actual_size[0]):
			x2 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
	
	
def on_y1_changed(val):
	global y1
	try:
		x = int(val)
		if(x >= 0 and x <= actual_size[1]):
			y1 = x
			print(f'{x1}, {x2}, {y1}, {y2}')
	except:
		pass
		
def on_y2_changed(val):
	global y2
	try:
		x = int(val)
		if(x >= y1 and x <= actual_size[1]):
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
		



def zoom_done(job):
	global cur_task
	global actual_size
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
		actual_size = [int(scale * actual_size[0]), int(scale * actual_size[1])]
		label.setText(f'{actual_size[0]} x {actual_size[1]}')
	if cur_task == 'cropp':
		pass
		


def on_dir_changed(text):
	global dir_name
	dir_name = text
	
	
def on_file_changed(text):
	global file_name
	file_name = text

def value_changed(i):
	try:
		e = int(i)
		if(e >= 0 and e <= 66):
			global exposure_time
			exposure_time = e *1000
			picam2.set_controls({"ExposureTime" : e *1000})
			
	except:
		pass
		
def on_time_changed(i):
	try:
		e = int(i)
		if(e >= 0):
			global capture_time
			capture_time = e
			
	except:
		pass		


def text_changed(val):
	try:
		print(val)
		global lens_pos
		val = float(val)/100.0
		if 1.0/float(val) <= 32 and 1.0/float(val) > 0:
			lens_pos = 1.0/float(val)
			#print(val + ' ' + lens_pos)
			picam2.set_controls({'LensPosition' : lens_pos})
			return
		elif int(val) == 0:
			lens_pos = 0
			#print(val + ' ' + lens_pos)
			picam2.set_controls({'LensPosition' : 0.0})
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
focalDistEdit.setMaxLength(5)
focalDistEdit.setPlaceholderText('Enter focal distance (min 3.2 cm)')
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


label = QLabel('1532 x 864')
label.setFixedSize(300, 20)

dir_edit = QLineEdit()
dir_edit.setMaxLength(30)
dir_edit.setPlaceholderText('Change directory name')
dir_edit.textEdited.connect(on_dir_changed)

file_edit = QLineEdit()
file_edit.setMaxLength(30)
file_edit.setPlaceholderText('Change file name')
file_edit.textEdited.connect(on_file_changed)

time_edit = QLineEdit()
time_edit.setMaxLength(30)
time_edit.setPlaceholderText('Change capture time')
time_edit.textEdited.connect(on_time_changed)


layout = QHBoxLayout()

layout_h = QHBoxLayout()
layout_h.addWidget(dir_edit)
layout_h.addWidget(file_edit)
layout_h.addWidget(time_edit)
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
qpicamera2.set_overlay(overlay)
window.show()


app.exec()


