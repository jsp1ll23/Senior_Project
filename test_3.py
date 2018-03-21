import os
import time

os.system("pd \"distortion.pd\" &")
time.sleep(5)
os.system("pkill pd &")
