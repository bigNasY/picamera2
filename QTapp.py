from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform, controls
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from picamera2.previews.qt import QGlPicamera2
import cv2



exposure_time = 100
scale = 1.05
picam2 = Picamera2()
mode = picam2.sensor_modes[0]
config = picam2.create_preview_configuration(main={"size" : (1280, 720)}, sensor={'output_size' : mode['size'], 'bit_depth' : mode['bit_depth']}, transform=Transform(vflip=True))
picam2.align_configuration(config)
picam2.configure(config)
picam2.set_controls({"FrameRate" : 50})





def on_button1_clicked():
	button1.setEnabled(False)
	global scale
	scale=0.95
	picam2.capture_metadata(signal_function=qpicamera2.signal_done)
	


def on_button2_clicked():
	button2.setEnabled(False)
	global scale
	scale = 1.05
	picam2.capture_metadata(signal_function=qpicamera2.signal_done)
	

	
	
	
	



def zoom_done(job):
	result = picam2.wait(job)
	full_res = picam2.camera_properties['PixelArraySize']
	size = result['ScalerCrop'][2:]
	newSize = [int(s * scale) for s in size]
	offset = [(r - s) // 2 for r, s in zip(full_res, newSize)]
	picam2.set_controls({'ScalerCrop' : offset+newSize})
	button1.setEnabled(True)
	button2.setEnabled(True)
	







app = QApplication([])
qpicamera2 = QGlPicamera2(picam2, width=800, height=600, keep_ar=False)

button1 = QPushButton("Click to zoom")
window = QWidget()
qpicamera2.done_signal.connect(zoom_done)
button1.clicked.connect(on_button1_clicked)


button2 = QPushButton("Click to zoom out")

button2.clicked.connect(on_button2_clicked)


layout_v = QVBoxLayout()
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button1)
layout_v.addWidget(button2)



qpicamera2.setWindowTitle("sigma")
window.setLayout(layout_v)
window.resize(640, 480)
picam2.start()
window.show()
app.exec()


