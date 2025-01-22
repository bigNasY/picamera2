from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from libcamera import Transform
import cv2
import time


def main():
    picam2 = Picamera2()
    mode = picam2.sensor_modes[0]
    config = picam2.create_preview_configuration(main={"size": (800, 640)}, sensor={
                                                 'output_size': mode['size'], 'bit_depth': mode['bit_depth']}, transform=Transform(vflip=True))
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.set_controls({"FrameRate": 50})
    # fps_image(picam2)
    fps_video(picam2)


def fps_image(picam2):
    # test fps at 50
    picam2.start()
    t_end = time.time() + 10
    count = 0
    while time.time() < t_end:
        picam2.capture_array("main")
        count += 1
    picam2.stop()

    fps = count/10
    print(f'FPS: {fps}')


def fps_video(picam2):
    # test framerate with a video recording
    picam2.start()
    encoder = H264Encoder(bitrate=10000000)
    picam2.start_recording(encoder, 'test.h264')
    time.sleep(10)
    picam2.stop_recording()

    vid = cv2.VideoCapture('/home/bob/Bookshelf/test.h264')
    count = 0
    success = 1
    while success:
        success, image = vid.read()
        count += 1

    fps = count/10
    print(f'FPS: {fps}')


if __name__ == "__main__":
    main()
