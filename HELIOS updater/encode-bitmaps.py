
"""
This is a way to save the startup time when running img2py on lots of
files...
"""

from wx.tools import img2py

command_lines = [
    "-F -n Exit images/exit.png images.py",
    "-a -F -n Reload images/reload.png images.py",
    "-a -F -n Splash images/splash.png images.py",
    "-a -F -n Select images/select.png images.py",
    "-a -F -n Select2 images/select2.png images.py",
    "-a -F -n Close images/close.png images.py",
    "-a -F -n Close2 images/close2.png images.py",
    "-a -F -n Bg images/bg.png images.py",
    "-a -F -n Loading images/loading.gif images.py",
    "-a -F -n Check images/check.gif images.py",
    "-a -F -n Bg images/bg.png images.py",
    "-a -F -n Info images/info.png images.py",
    "-a -F -i -n Icon images/icon-256.png images.py",
    ]

if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

