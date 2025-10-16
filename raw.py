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
from PIL import Image
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import bluetooth
import RPi.GPIO as GPIO

style.use('fivethirtyeight')
#fig, ax = plt.subplots()
#canvas = FigureCanvas(fig)
matplotlib.use('Qt5Agg')
picam2 = Picamera2()
cropped = False
xs = []
ys = []
modeNum = 0
still = 1000
t_start = 0
t_end = 0
recording = False
file_name = 'img'
cur_task = ''
dir_name = 'images'
path = ''
app = QApplication([])
overlay = np.zeros((721, 1281, 4), dtype=np.uint8)
capture_time = 1

target = 0
cur_task = ''
running = False
min_exp, max_exp, def_exp = picam2.camera_controls['ExposureTime']
exposure_time = (max_exp + min_exp) // 2
count = 1
frame_rate = 30
lens_pos = 32
stills = 1
x1 = 0
x2 = 4608
y1 = 0
y2 = 2592
mode = picam2.sensor_modes[0]
actual_size = [i for i in mode['size']]
config = picam2.create_preview_configuration(sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False), raw={'format' : mode['unpacked'], 'size' : mode['size']})
picam2.align_configuration(config)
picam2.configure(config)
picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, 'LensPosition' : lens_pos})



GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12,1000)
brightness = 50
pwm.start(brightness)


class Worker(QObject):
    finished = pyqtSignal()
    
    
    def run(self):
        global count
        fps_count = count
        store = []
        #change_config(picam2.create_still_configuration(sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False), raw={'format' : picam2.sensor_modes[0]['unpacked'], 'size' : mode['size']}))
        time.sleep(3)
        t_end = time.time() + capture_time *1.0
        print('checkpoint ')
        if cropped:
            while time.time() <= t_end:
                ts = time.time()
                r = picam2.capture_array('raw')
                r = r.view(np.uint16).reshape(mode['size'][1], mode['size'][0])
                r = np.array(r[y1 : y2, x1 : x2])
                r.tofile(f'{dir_name}/{file_name + str(count)}.raw')
                te = time.time()
                fps = (1/(te-ts))
                label2.setText(f'FPS: {int(fps)}')
                count += 1
            
        else:
            while time.time() <= t_end:
                ts = time.time()
                r = picam2.capture_array('raw')
                r = r.view(np.uint16).reshape(mode['size'][1], mode['size'][0])
                count += 1
                r.tofile(f'{dir_name}/{file_name + str(count)}.raw')
                te = time.time()
                fps = (1/(te-ts))
                
      
           
        
        #print(f'len: {len(store)}')
        print(f'actual fps: {(count-fps_count)/capture_time}')
         
       
  
        self.finished.emit()
        

        
class Worker3(QObject):
	finished = pyqtSignal()
	
	def run(self):
		
		arr = picam2.capture_array('raw')
		print(np.amax(arr))
		arr = arr.view(np.uint16).reshape(mode['size'][1], mode['size'][0])
		
		if cropped:
			arr = np.array(arr[y1 : y2, x1 : x2])
		
		print(arr.shape) 
		print(np.amax(arr))
		
		
		arr.tofile(f'{dir_name}/{file_name + str(still)}.raw') 
		#cv2.imwrite(f'{dir_name}/{file_name + str(still)}.jpg', cv2.cvtColor(arr, cv2.COLOR_BAYER_RG2BGR))
        
		self.finished.emit()
        
class Worker2(QObject):
	finished = pyqtSignal()
    

    
    
	def run(self):
		global xs
		global ys
		global ax
 

       
		count = 1
		while True:
			if recording:
				break
			time.sleep(0.5)
			i = picam2.capture_array(f'raw')
			i = i.view(np.uint16).reshape(mode['size'][1], mode['size'][0])
			if cropped:
				i = i[y1 : y2 , x1 : x2]
               
			mean_intensity = np.mean(i)
              
			client_sock.send(str(mean_intensity))
                
		self.finished.emit()
          
            
     
            

		
		
thread = QThread()
thread2 = QThread()
thread3 = QThread()
worker = Worker()
worker2 = Worker2()
worker3 = Worker3()



def change_config(cfg):
    picam2.stop()
    picam2.configure(cfg)
    offset = [x1, y1]
    size = [x2-x1, y2-y1]
    if cropped:	
        picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos, 'ScalerCrop' : offset+size})
    else:
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
	global modeNum
	global actual_size
	global overlay
	global cropped
	cropped = False
	modeNum = 2
	cropper.setEnabled(True)
	actual_size = [4608, 2592]
	label.setText('4608 x 2592')
	button3.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[2]
	button1.setEnabled(True)
	button2.setEnabled(True)
	
	config = picam2.create_preview_configuration(sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False), raw={'format' : picam2.sensor_modes[2]['unpacked'], 'size' : mode['size']})
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	
	button4.setEnabled(True)
	button5.setEnabled(True)
	
	
def on_button4_clicked():
	global mode
	global modeNum
	global actual_size
	global overlay
	global cropped
	cropped = False
	cropper.setEnabled(False)
	modeNum = 0
	actual_size = [1536, 864]
	label.setText('1536 x 864')
	button4.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[0]
	config = picam2.create_preview_configuration(sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False), raw={'format' : picam2.sensor_modes[0]['unpacked'], 'size' : mode['size']})
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	button1.setEnabled(False)
	button2.setEnabled(False)

	button3.setEnabled(True)
	button5.setEnabled(True)

	
	
	
def on_button5_clicked():
	global mode
	global modeNum
	global actual_size
	global overlay
	global cropped 
	cropped = False
	cropper.setEnabled(False)
	modeNum = 1
	actual_size = [2304, 1296]
	label.setText('2304 x 1296')
	button5.setEnabled(False)
	picam2.stop()
	mode = picam2.sensor_modes[1]
	button1.setEnabled(False)
	button2.setEnabled(False)
	config = picam2.create_preview_configuration(sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=False), raw={'format' : picam2.sensor_modes[1]['unpacked'], 'size' : mode['size']})
	picam2.align_configuration(config)
	picam2.configure(config)
	picam2.set_controls({"FrameRate" : frame_rate, 'ExposureTime' : exposure_time, "LensPosition" : lens_pos})
	picam2.start()
	qpicamera2.set_overlay(overlay)
	button3.setEnabled(True)
	button4.setEnabled(True)
	
	
def on_button6_clicked():
	global cur_task
	global still
	cur_task = 'fr'
	cfg = picam2.create_still_configuration(main={'size' : actual_size}, transform=Transform(vflip=False))
	
	global path
	cwd = os.getcwd()
	try:
		path = f'{cwd}/{dir_name}'
		os.mkdir(path)
		#picam2.switch_mode_and_capture_file(cfg, f'{path}/{file_name + str(still)}.jpg', signal_function=qpicamera2.signal_done)
	except:
		pass
		#picam2.switch_mode_and_capture_file(cfg, f'{path}/{file_name + str(still)}.jpg', signal_function=qpicamera2.signal_done)
	
	worker3.moveToThread(thread3)
	thread3.started.connect(worker3.run)
	worker3.finished.connect(thread3.quit)
	thread3.start()
	still += 1
	
	
	
	
def on_button7_clicked():
	global path
	global ani
	global recording 
	recording = True
	#ani.pause()
	
	cwd = os.getcwd()
	try:
		path = f'{cwd}/{dir_name}'
		os.mkdir(path)
	except:
		pass

	thread.start()

def on_thread_finish():
	global thread2
	global recording
	recording = False
	thread2.start()
	#ani.resume()
	
def on_x1_changed(val):
	if(modeNum == 2):
		global x1
		ratio = 1280 / actual_size[0] 
		#print(ratio)
		
		try:
			overlay[:1280, math.floor(x1*ratio)] = (0, 0, 0, 0)
			x = int(val)
			
			if(x >= 0 and x <= actual_size[0]):
				
				x1 = x
				overlay[:1280, math.floor(x*ratio)] = (255, 0, 0, 255)
				qpicamera2.set_overlay(overlay)
			
		except:
			pass
		
def on_x2_changed(val):
	if(modeNum == 2):
		global x2
		
		ratio = 1280 / actual_size[0] 
		
		
		
		try:
			overlay[:1280, math.floor(x2*ratio)] = (0, 0, 0, 0)
			x = int(val)
			x2 = x
			
			if(x >= x1 and x <= actual_size[0]):
				
				overlay[:1280, math.floor(x*ratio)] = (255, 0, 0, 255)
				qpicamera2.set_overlay(overlay)
				
			
		except:
			pass
	
	
def on_y1_changed(val):
	if(modeNum == 2):
		global y1
		ratio = 720 / actual_size[1] 
		
		
		try:
			overlay[math.floor(y1*ratio), :1280] = (0, 0, 0, 0)
			x = int(val)
			
			if(x >= 0 and x <= actual_size[1]):
				y1 = x
				overlay[math.floor(x*ratio), :1280] = (255, 0, 0, 255)
				qpicamera2.set_overlay(overlay)
				
		except:
			pass
		
def on_y2_changed(val):
	if(modeNum == 2):
		global y2
		ratio = 720 / actual_size[1] 
		
		try:
			overlay[math.floor(y2*ratio), :1280] = (0, 0, 0, 0)
			x = int(val)
			
			if(x >= y1 and x <= actual_size[1]):
				y2 = x
				overlay[math.floor(x*ratio), :1280] = (255, 0, 0, 255)
				qpicamera2.set_overlay(overlay)
				
		except:
			pass
	

def on_cropper_clicked():
	global cur_task
	global actual_size
	global cropped
	global mode
	global modeNum
	global actual_size
	global overlay
	ratioY = 720 / actual_size[1] 
	ratioX = 1280 / actual_size[0] 
	overlay[math.floor(y2*ratioY), :1280] = (0, 0, 0, 0)
	overlay[math.floor(y1*ratioY), :1280] = (0, 0, 0, 0)
	overlay[:1280, math.floor(x1*ratioX)] = (0, 0, 0, 0)
	overlay[:1280, math.floor(x2*ratioX)] = (0, 0, 0, 0)
	qpicamera2.set_overlay(overlay)
	cropped = True
	cur_task = 'crop'

	try:
		full_res = picam2.sensor_resolution
		offset = [x1,y1]
		size = [x2-x1, y2-y1]
		actual_size = size
		
		picam2.set_controls({'ScalerCrop' : offset+size})
		label.setText(f'{size[0]} x {size[1]}')
		
	except:
		pass
		



def zoom_done(job):
	global cur_task
	global actual_size
	global x1, y1, x2, y2
	result = picam2.wait(job)
	if cur_task == 'zoom':
		full_res = picam2.camera_properties['PixelArraySize']
		size = result['ScalerCrop'][2:]
		
		newSize = [int(s * scale) for s in size]
		offset = [(r - s) // 2 for r, s in zip(full_res, newSize)]
		picam2.set_controls({'ScalerCrop' : offset+newSize})
		button1.setEnabled(True)
		button2.setEnabled(True)
		x1 = 4608 - (scale*actual_size[0])
		x2 = scale*actual_size[size]
		y1 = 2592 - (scale*actual_size[1])
		y2 = scale*actual_size[1]
		actual_size = [int(scale * actual_size[0]), int(scale * actual_size[1])]
		
		label.setText(f'{actual_size[0]} x {actual_size[1]}')


def on_dir_changed():
	global dir_name
	options = QFileDialog.Options()
	options |= QFileDialog.DontUseNativeDialog
	directory = QFileDialog.getExistingDirectory(dir_edit, "Select Directory", os.getcwd(), options=options,)
	if directory:
		print(directory)
		dir_name = directory
		print(dir_name)
		dir_edit.setText(directory)
		
	
	
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

	except:
		pass

def set_level(val):
	global brightness
	try:
		if int(val):
			if int(val) >= 0 and int(val) <= 100:
				brightness = int(val)
	except:
		brightness = 0
		return



def set_cycle():
	global pwm
	pwm.ChangeDutyCycle(brightness)


qpicamera2 = QGlPicamera2(picam2, width=1280, height=720, keep_ar=False)


button1 = QPushButton("Click to zoom in")
window = QWidget()
qpicamera2.done_signal.connect(zoom_done)
button1.clicked.connect(on_button1_clicked)


button2 = QPushButton("Click to zoom out")
button2.clicked.connect(on_button2_clicked)
button1.setEnabled(False)
button2.setEnabled(False)
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



label = QLabel('1536 x 864')
label.setFixedSize(150, 20)

label2 = QLabel('FPS: ')
label2.setFixedSize(150, 20)

'''
dir_edit = QLineEdit()
dir_edit.setMaxLength(30)
dir_edit.setPlaceholderText('Change directory name')
dir_edit.textEdited.connect(on_dir_changed)
'''
dir_edit = QPushButton('select directory')
dir_edit.clicked.connect(on_dir_changed)

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


layout_h3 = QHBoxLayout()
layout_h3.addWidget(label)
layout_h3.addWidget(label2)

layout_v3 = QHBoxLayout()
layout_v3.addWidget(button4)
layout_v3.addWidget(button5)
layout_v3.addWidget(button3)

layout_v4 = QHBoxLayout()
layout_v4.addWidget(frameEdit)
layout_v4.addWidget(button6)

layout_v = QVBoxLayout()
layout_v.setSpacing(10)
layout_v.addLayout(layout_h3)
layout_v.addWidget(qpicamera2)

layout_v.addLayout(layout_v3)
layout_v.addWidget(focalDistEdit)
layout_v.addWidget(expTimeSlider)
layout_v.addLayout(layout_v4)
layout.addLayout(layout_v)
layout_v.addLayout(layout_h)
layout_v.addLayout(layout_h2)

bright = QLineEdit()
bright.setMaxLength(3)
bright.setPlaceholderText("Adjust Intensity")
set_br = QPushButton("Set Intensity")
bright.textEdited.connect(set_level)
set_br.clicked.connect(set_cycle)

layout_h4 = QHBoxLayout()
layout_h4.addWidget(bright)
layout_h4.addWidget(set_br)

layout_v.addLayout(layout_h4)



qpicamera2.setWindowTitle("sigma")
window.setLayout(layout)
window.resize(800, 800)
picam2.start()
qpicamera2.set_overlay(overlay)
window.show()


worker.moveToThread(thread)
thread.started.connect(worker.run)
worker.finished.connect(on_thread_finish)
worker.finished.connect(thread.quit)

worker2.moveToThread(thread2)
thread2.started.connect(worker2.run)
worker2.finished.connect(thread2.quit)
thread2.start()



server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_sock.bind(("", port))
server_sock.listen(1)

print('waiting')

client_sock, address = server_sock.accept()

print('connected')




app.exec()
client_sock.close()
server_sock.close()
pwm.stop()



