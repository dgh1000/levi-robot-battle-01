import math
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

class RenderArea(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent) 
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.antialiased = True
        self.rotation = 0.0
        self.t = 0.0
        self.deltaT = -1.0
        self.radius = 100.0
        self.center = QtCore.QPointF(200, 200)

    def minimumSizeHint(self):
        return QtCore.QSize(400, 400)

    def sizeHint(self):
        return QtCore.QSize(750, 750)

    def reverseDir(self):
        self.deltaT = -self.deltaT
        
    def paintEvent(self, event):

        def computeVec(ang):
            return QtCore.QPointF(math.cos(ang), math.sin(ang))


        ang = 2*math.pi*self.t/1000.0
        pp1 = self.center + self.radius * computeVec(ang)
        pen1 = QtGui.QPen(self.palette().dark().color())
        pen1.setWidth(5)
        painter = QtGui.QPainter(self)
        painter.setPen(pen1)
        if self.antialiased:
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawLine(self.center, pp1)

    def timeUpdate(self):
        self.t += self.deltaT * 16.0
        self.update()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.renderArea = RenderArea()
        lo = QtWidgets.QHBoxLayout()
        lo.addWidget(self.renderArea)
        self.setLayout(lo)
        self.setWindowTitle("Drawing")
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.renderArea.timeUpdate)
        self.timer.start(30)

    def keyPressEvent(self, evt):
        self.renderArea.reverseDir()
        if evt.key() == QtCore.Qt.Key_A:
            self.renderArea.reverseDir()
        
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    app.exec_()
