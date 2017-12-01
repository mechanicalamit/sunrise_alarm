"""
Hardware Driver Class

Input : Color/Sound profile, None for all Off
Output : Light and Sound

BCM Pins
18 = green
17 = blue
22 = red
"""

import sys
import time

class Light_Sound(object):

    def __init__(self, enable_hw=False, enable_pyqt=False, printer=None):
        self.enable_hw = enable_hw
        self.enable_pyqt = enable_pyqt
        self.printer = printer

        if self.enable_hw:
            pass

        if self.enable_pyqt:
            from PyQt5 import QtGui, QtWidgets
            class ColorWindow(QtWidgets.QWidget):
                from PyQt5 import QtGui, QtWidgets

                def __init__(self):
                    super().__init__()
                    self.init()

                def init(self):

                    self.col = QtGui.QColor(0, 0, 0)

                    self.setGeometry(300, 300, 280, 170)
                    self.setWindowTitle('Light and Sound')
                    self.setStyleSheet("QWidget { background-color: %s }" %
                        self.col.name())

                    self.show()

                def set_col(self, rgbvals):
                    self.col = QtGui.QColor(rgbvals[0], rgbvals[1], rgbvals[2])
                    self.setStyleSheet("QWidget { background-color: %s }" %
                        self.col.name())
                # End of class ColorWindow

            self.app = QtWidgets.QApplication(sys.argv)
            self.ColorWindow = ColorWindow()

    def blink_red_twice(self):
        self.set_rgb((1,0,0))
        time.sleep(0.5)
        self.set_rgb((0,0,0))
        time.sleep(0.5)
        self.set_rgb((1,0,0))
        time.sleep(0.5)
        self.set_rgb((0,0,0))

    def blink_green_twice(self):
        self.set_rgb((0,1,0))
        time.sleep(0.5)
        self.set_rgb((0,0,0))
        time.sleep(0.5)
        self.set_rgb((0,1,0))
        time.sleep(0.5)
        self.set_rgb((0,0,0))

    def set_rgb(self, rgbvals):
        if self.enable_hw:
            self.changer(22, rgbvals[0]/255)
            self.changer(18, rgbvals[1]/255)
            self.changer(17, rgbvals[2]/255)

        if self.enable_pyqt:
            self.ColorWindow.set_col(rgbvals)
            self.app.processEvents()

        if self.printer:
            self.printer.print(rgbvals)

    def alloff(self):
        self.set_rgb((0,0,0))

    def changer(self, pin, amount):
        f = open('/dev/pi-blaster', 'w')
        f.write('%d=%s\n'%(pin, str(amount)))
        f.close


# If called directly, Run a light loop to test/debug
if __name__ == '__main__' :
    import time
    liso = Light_Sound(enable_hw=True, enable_pyqt=True)
    for i in range(0,256):
        liso.set_rgb((i, 0, 0))
        time.sleep(0.01)
    for i in range(255,0, -1):
        liso.set_rgb((i, 0, 0))
        time.sleep(0.01)
    for i in range(0,256):
        liso.set_rgb((0, i, 0))
        time.sleep(0.01)
    for i in range(255,0, -1):
        liso.set_rgb((0, i, 0))
        time.sleep(0.01)
    for i in range(0,256):
        liso.set_rgb((0, 0, i))
        time.sleep(0.01)
    for i in range(255,0, -1):
        liso.set_rgb((0, 0, i))
        time.sleep(0.01)

