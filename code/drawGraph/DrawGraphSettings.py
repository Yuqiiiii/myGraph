class DrawGraphSetting:
    def __init__(self):
        self.dpi = 72
        self.K = 3
        # Put the images you want to process in the following folders
        self.maskPath = '../image/mask/'
        self.rawPath = '../image/raw/'
        # The graphs will be put into the following folders
        self.maskGraphPath = '../image/graph/mask/'
        self.rawGraphPath = '../image/graph/raw/'

