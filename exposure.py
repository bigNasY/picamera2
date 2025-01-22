from picamera2 import Picamera2, Preview
from libcamera import Transform
import cv2
import time


def main():
    picam2 = Picamera2()
    mode = picam2.sensor_modes[0]
    config = picam2.create_preview_configuration(main={"size": (1280, 720), "format": "RGB888"}, sensor={
                                                 'output_size': mode['size'], 'bit_depth': mode['bit_depth']}, transform=Transform(vflip=True))
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({"ExposureTime": 1000})
    picam2.start()
    low_exp(picam2)
    high_exp(picam2)


def low_exp(picam2):
    # capture low exposre time (1ms)
    img = picam2.capture_array()
    time.sleep(2)
    # cv2.imshow("low ET", img) -- This is being weird
    cv2.imwrite('1ms.jpg', img)


def high_exp(picam2):
    # capture high exposure time (100ms)
    picam2.set_controls({"ExposureTime": 100000})
    time.sleep(2)
    img2 = picam2.capture_array()
    time.sleep(2)
    # cv2.imshow("high ET", img2)
    cv2.imwrite("100ms.jpg", img2)


if __name__ == "__main__":
    main()
