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

cur_dir = os.getcwd()
t_start = 0
t_end = 0
recording = False
file_name = ''
cur_task = ''
app = QApplication([])
capture_time = 5
scale = 1.05
picam2 = Picamera2()
target = 0
cur_task = ''
min_exp, max_exp, def_exp = picam2.camera_controls['ExposureTime']
exposure_time = (max_exp + min_exp) // 2
scale = 1.05
frame_rate = 30
lens_pos = 32
x1 = 0
x2 = 4608
y1 = 0
y2 = 2592
mode = picam2.sensor_modes[0]
actual_size = [i for i in mode['size']]
config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False))
picam2.align_configuration(config)
picam2.configure(config)
picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, 'LensPosition' : 0.0})



	
	
def on_button7_clicked():
	t_end = time.time() + 5.0
    
	
	while time.time() <= t_end:
		picam2.capture_file(f'{cur_dir}/images/img{str(time.time())[-4:]}.jpg', signal_function=qpicamera2.signal_done)
	


def zoom_done(job):
	global cur_task
	global actual_size
	result = picam2.wait(job)
	


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


window = QWidget()
qpicamera2.done_signal.connect(zoom_done)


button7 = QPushButton('Start continuous image capture')
button7.clicked.connect(on_button7_clicked)



frameEdit = QLineEdit()
frameEdit.setMaxLength(3)
frameEdit.setPlaceholderText('Enter Frame Rate')
frameEdit.textEdited.connect(frame_text_changed)



label = QLabel('1536 x 864')
label.setFixedSize(300, 20)


layout = QHBoxLayout()












layout_v = QVBoxLayout()
layout_v.setSpacing(10)
layout_v.addWidget(label)
layout_v.addWidget(qpicamera2)
layout_v.addWidget(frameEdit)
layout_v.addWidget(button7)

layout.addLayout(layout_v)




qpicamera2.setWindowTitle("sigma")
window.setLayout(layout)
window.resize(800, 800)
picam2.start()
window.show()
app.exec()



