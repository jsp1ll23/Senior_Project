import os
import subprocess

pd = "menu://applications/Multimedia"
pd_file = "/home/pi/distortion.pd"
subprocess.Popen("%s %s" % (pd, pd_file))
