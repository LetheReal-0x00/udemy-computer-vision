import sys
import random
import argparse

from PySide2 import QtCore, QtWidgets, QtGui
from skvideo.io import vread

from detector import MotionDetector

class QtDemo(QtWidgets.QWidget):
    def __init__(self, frames):
        super().__init__()

        self.frames = frames

        self.current_frame = 0

        # Configure image label
        self.img_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)

        # h, w, c = self.frames[0].shape
        # if c == 1:
        #     img = QtGui.QImage(self.frames[0], w, h, QtGui.QImage.Format_Grayscale8)
        # else:
        #     img = QtGui.QImage(self.frames[0], w, h, QtGui.QImage.Format_RGB888)
        # self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

        # Configure slider
        self.frame_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.frame_slider.setTickInterval(1)
        self.frame_slider.setMinimum(0)
        self.frame_slider.setMaximum(self.frames.shape[0]-1)
        self.frame_slider.setValue(400)

        # motion detector class
        self.motion_detector = MotionDetector(frames=self.frames)

        # starts at frame 400
        self.motion_detector.register_blobs(400)
        h, w, c = self.frames[400].shape
        if c == 1:
            img = QtGui.QImage(self.frames[400], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[400], w, h, QtGui.QImage.Format_RGB888)

        painter = QtGui.QPainter(img)
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth = 3
        painter.setPen(pen)
        for blob in self.motion_detector.blobs:
            x, y, dx, dy = self.motion_detector.get_qt_bounding_box(blob)
            painter.drawRect(x, y, dx, dy)
        painter.end()

        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.img_label)
        self.layout.addWidget(self.frame_slider)

        # Connect functions
        self.frame_slider.sliderMoved.connect(self.on_move)


    @QtCore.Slot()
    def on_move(self, pos):
        self.current_frame = pos
        self.motion_detector.register_blobs(self.current_frame)
        h, w, c = self.frames[self.current_frame].shape
        if c == 1:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_RGB888)

        # TODO: draw bounding somehow?
        painter = QtGui.QPainter(img)
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth = 3
        painter.setPen(pen)
        for blob in self.motion_detector.blobs:
            x, y, dx, dy = self.motion_detector.get_qt_bounding_box(blob)
            painter.drawRect(x, y, dx, dy)
        painter.end()
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Demo for loading video with Qt5.")
    parser.add_argument("video_path", metavar='PATH_TO_VIDEO', type=str)
    parser.add_argument("--num_frames", metavar='n', type=int, default=-1)
    parser.add_argument("--grey", metavar='True/False', type=str, default=False)
    args = parser.parse_args()

    num_frames = args.num_frames

    if num_frames > 0:
        frames = vread(args.video_path, num_frames=num_frames, as_grey=args.grey)
    else:
        frames = vread(args.video_path, as_grey=args.grey)

    app = QtWidgets.QApplication([])

    widget = QtDemo(frames)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())

    # frames = vread('./east_parking_reduced_size.mp4')
    # detector = MotionDetector(frames)
    # detector.register_blobs(400)
    # x, y, dx, dy = detector.get_qt_bounding_box(detector.blobs[0])
    # print(x, y, dx, dy)