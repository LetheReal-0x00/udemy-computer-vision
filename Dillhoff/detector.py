import numpy as np

from skimage.color import rgb2gray
from skimage.measure import label, regionprops
from skimage.morphology import dilation

class MotionDetector:
    def __init__(self, frames, hysteresis = (0.1, 0.35), threshold = 0.05, distance = 15, skips = 10, num_obj = 99):
        self.frames = frames
        self.hysteresis = hysteresis    # not sure how to use
        self.threshold = threshold
        self.dilation_distance = (distance, distance)
        self.skips = skips  # not sure how to use
        self.num_obj = num_obj

        self.blobs = []

    def register_blobs(self, idx):
        # needs at least 3 frames
        if idx < 2:
            idx = 2

        # finding frame diff
        ppframe = rgb2gray(self.frames[idx-2])
        pframe = rgb2gray(self.frames[idx-1])
        cframe = rgb2gray(self.frames[idx])
        diff1 = np.abs(cframe - pframe)
        diff2 = np.abs(pframe - ppframe)

        # quantify frame diff to motion regions
        motion_frame = np.minimum(diff1, diff2)
        thresh_frame = (motion_frame > self.threshold)
        dilated_frame = dilation(thresh_frame, np.ones(self.dilation_distance))
        label_frame = label(dilated_frame)
        regions = regionprops(label_frame)

        # make sure it doesn't go out of bound
        limit = len(regions) if (len(regions) < self.num_obj) else self.num_obj

        # store it somewhere
        self.blobs = [regions[i] for i in range(limit)]

    def get_qt_bounding_box(self, blob):
        minr, minc, maxr, maxc = blob.bbox
        y = minr
        x = minc
        dy = maxr - minr
        dx = maxc - minc
        return x, y, dx, dy

class KalmanFilter:
    def __init__(self):
        pass