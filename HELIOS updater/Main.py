#!/usr/bin/env python

#ESP8266 Flasher by TheHackLife

import wx
import wx.adv
import wx.lib.inspection
import wx.lib.mixins.inspection

import sys
import os
import esptool
import threading
import json
import images as images
from serial import SerialException
from serial.tools import list_ports
from esptool import ESPLoader
from esptool import NotImplementedInROMError
from esptool import FatalError
from argparse import Namespace
import time
from wx.lib.agw.shapedbutton import SButton, SBitmapButton
from wx.lib.agw.shapedbutton import SBitmapToggleButton, SBitmapTextToggleButton
from wx.adv import Animation, AnimationCtrl
from wx.lib.newevent import NewEvent
import sys
import os
from contextlib import redirect_stdout
loc = wx.Locale()
 
__version__ = "4.0"
__flash_help__ = '''
<p>This setting is highly dependent on your device!<p>
<p>
  Details at <a style="color: #004CE5;"
        href="https://www.esp32.com/viewtopic.php?p=5523&sid=08ef44e13610ecf2a2a33bb173b0fd5c#p5523">http://bit.ly/2v5Rd32</a>
  and in the <a style="color: #004CE5;" href="https://github.com/espressif/esptool/#flash-modes">esptool
  documentation</a>
<ul>
  <li>Most ESP32 and ESP8266 ESP-12 use DIO.</li>
  <li>Most ESP8266 ESP-01/07 use QIO.</li>
  <li>ESP8285 requires DOUT.</li>
</ul>
</p>
'''
globaldir = ""
uploaded = 0;
command = []
wxStdOut, EVT_STDDOUT= NewEvent()
wxWorkerDone, EVT_WORKER_DONE= NewEvent()

def done(self):
    #anim2 = Animation(images.Check.GetBitmap())
    #ctrl2 = AnimationCtrl(self, 1, anim2, pos = (288,291))
    #ctrl2.Play()
    #self.picture = wx.StaticBitmap(self.panel,size=(30,30),pos=(288,291))
    self.picture.SetBitmap(images.Check.GetBitmap())

def scale_bitmap(impath, width, height):
    image = wx.Image(impath, wx.BITMAP_TYPE_ANY)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result

class Panel(wx.Panel):
    def __init__(self, parent, impath=None):
        super(Panel, self).__init__(parent, -1)

class MySplashScreen(wx.adv.SplashScreen):
    def __init__(self):
        bitmap = images.Splash.GetBitmap()
        wx.adv.SplashScreen.__init__(self, bitmap, wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT, 2500, None, -1, style=wx.BORDER_NONE)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.__fc = wx.CallLater(2000, self._show_main)

    def _on_close(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.__fc.IsRunning():
            self.__fc.Stop()
            self._show_main()
    
    def _show_main(self):
        frame = MyFrame(None, imgpath=r'') 
        frame.Show()
        frame.Centre()
        if self.__fc.IsRunning():
            self.Raise()


class App(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName("TheHackLife Helios Updater")
        self.frame = MySplashScreen()
        self.frame.Show()
        loc.Init(wx.LANGUAGE_DEFAULT)
        #self.frame = MyFrame(None, imgpath=r'') 
        #self.frame.Show(True)
        return True

class FlashingThread(threading.Thread):
    def __init__(self, se, dir):
        threading.Thread.__init__(self)
        self.daemon = True
        self.se = se
        self.dir = dir
    def run(self):
        command.extend(["--baud", "921600", "--after", "no_reset", "write_flash", "--flash_mode", "dio", "0x00000", self.dir])
        with open('log.txt', 'w') as f:
            with redirect_stdout(f):
                #print("Command: esptool.py %s\n" % " ".join(command))
                print("Starting HELIOS updater by TheHackLife")
                print("dir is " + globaldir)
                esptool.main(command)
                evt = wxWorkerDone()
                wx.PostEvent(self.se, evt)
    
class MyFrame(wx.Frame):
    def __init__(self, parent, imgpath=None): 
        wx.Frame.__init__(self, parent, -1, style=wx.BORDER_NONE)
        self.panel = Panel(self, imgpath)
        self._init_ui()
        
        self.SetSize(599,395)
        self.SetPosition((0,0))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        self.Bind(EVT_WORKER_DONE, self.OnWorkerDone)

    def OnWorkerDone(self, event):
            print("done");
            done(self);
            myCursor= wx.Cursor(wx.CURSOR_DEFAULT)
            self.panel.SetCursor(myCursor)
    def _init_ui(self):
        def m_OpenPrintOnButtonClick(event):
            dlg = wx.FileDialog(None, "Seleccionar Firmware", wildcard="Firmware (*.bin)|*.bin", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            dlg.ShowModal()
            globaldir = dlg.GetPath().replace("'", "")
            if(globaldir != ""):
                #anim = Animation(images.Loading.GetBitmap())
                #self.ctrl = AnimationCtrl(self, 1, anim, pos = (288,291))
                #self.ctrl.Play()
                self.picture = wx.StaticBitmap(self.panel,size=(30,30),pos=(288,291))
                self.picture.SetBitmap(images.Loading.GetBitmap())
                myCursor= wx.Cursor(wx.CURSOR_WAIT)
                self.panel.SetCursor(myCursor)
                
                self.worker = FlashingThread(self, globaldir)
                self.worker.start()
        def closevent(event):
            self.Close()

        img1 = images.Select.GetBitmap()
        img2 = images.Select2.GetBitmap()
        asize = img1.GetSize()
        self.Btn = SBitmapButton(self.panel, 0,None, pos = (106,150), size = (asize[0]-2, asize[1]-2))
        self.Btn.SetBitmapLabel(img1)
        self.Btn.SetUseFocusIndicator(False)
        self.Btn.SetBitmapSelected(img2)
        c = wx.Cursor(wx.CURSOR_HAND) 
        self.Btn.SetCursor(c) 
        self.Btn.Bind(wx.EVT_BUTTON, m_OpenPrintOnButtonClick)
        
        img11 = images.Close.GetBitmap()
        img21 = images.Close2.GetBitmap()
        asize2 = img11.GetSize()
        self.Btn2 = SBitmapButton(self.panel, 0,None, pos = (551,0), size = (asize2[0]-1, asize2[1]-1))
        self.Btn2.SetBitmapLabel(img11)
        self.Btn2.SetUseFocusIndicator(False)
        self.Btn2.SetBitmapSelected(img21)
        self.Btn2.SetCursor(c) 
        self.Btn2.Bind(wx.EVT_BUTTON, closevent)

        
        bitmap = images.Bg.GetBitmap()
        self.control = wx.StaticBitmap(self, -1, bitmap)

# ---------------------------------------------------------------------------
def main():
    app = App(False)
    app.MainLoop()
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    __name__ = 'Main'
    main()

