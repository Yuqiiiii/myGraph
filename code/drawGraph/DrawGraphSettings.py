import sys
import os

from numpy.ma import sqrt


class DrawGraphSetting:
    def __init__(self):
        self.dpi = 72
        self.scaleTarget = 0.2  # m
        self.scaleStr = '200 mm'
        self.scanMag = 40/sqrt(16)

        # K is the maximum degree of each node
        # K corresponding to its K-nearest neighbors
        self.K = 3

        # Put the images you want to process in the following folders
        self.maskPath = os.path.join(sys.path[0], '../image/mask/')
        self.rawPath = os.path.join(sys.path[0], '../image/raw/')
        # The graphs will be put into the following folders
        self.maskGraphPath = os.path.join(sys.path[0], '../image/graph/mask/')
        self.rawGraphPath = os.path.join(sys.path[0], '../image/graph/raw/')
