import subprocess
import re

# Runs shell command to get all windows open
command = ["wmctrl -lG", "|", "awk ", "'{$2=""; $1=""; print $0}'"]
lines = subprocess.getoutput(command).split("\n")

# Adds windows to list
windows = []
for line in lines:
    line = line.replace("  ", " ")
    windows.append(line.split(" ", 2))

# Extracts only the x,y,height,width and name of all windows and prints them
for win in windows:
    wininfo = win[2]
    speclist = wininfo.split()
    x = speclist[0]
    y = speclist[1]
    width = speclist[2]
    height = speclist[3]
    machine_name = speclist[4]
    window_name = " ".join(speclist[5:])
    print("Window name: ", window_name, "X: ", x,
          "Y:", "Width: ", width, "Height: ", height)

'''
To resize a window:
wmctrl -r string -e 0,left,up,width,height

where string is a substring of the window's title, (left,up) are the desired screen coordinates of the upper left window's corner,
and (width,height) are the desired window's dimensions.
'''

# Resize a window by name (not all that reliable, should do it by window ID, but eh)


def resize_window(win_name, left, up, width, height):
    cmd = "wmctrl -r ", win_name, " -e 0,", left, ",", up, ",", width, ",", height
    cmd = "".join(cmd)
    print("GOT COMMAND: ", cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

