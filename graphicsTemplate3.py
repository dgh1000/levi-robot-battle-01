import math
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

class Cell():
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def getQRect(self):
        return QtCore.QRectF(self.pos.x(), self.pos.y(), self.size, self.size)

class RenderArea(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent) 
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.antialiased = True
        self.pos = QtCore.QPointF(200, 200)
        self.vel = QtCore.QPointF(0, 10)
        self.snake = []

    def minimumSizeHint(self):
        return QtCore.QSize(400, 400)

    def sizeHint(self):
        return QtCore.QSize(750, 750)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        for snake in self.snake:
            painter.drawRect(snake.getQRect())

    def createNewCell(self):
        self.pos += self.vel
        # Robot: r + 3 

        self.snake.append(Cell(QPointF(self.pos), 10))

    def timeUpdate(self):
        self.createNewCell()
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
        if evt.key() == QtCore.Qt.Key_W:
            self.renderArea.vel = QPointF(0, -10)
            self.renderArea.vel.setY(-10)
            self.renderArea.vel.setX(0) 
        if evt.key() == QtCore.Qt.Key_S:
            self.renderArea.vel.setY(10)
            self.renderArea.vel.setX(0) 
        if evt.key() == QtCore.Qt.Key_A:
            self.renderArea.vel.setX(-10)
            self.renderArea.vel.setY(0) 
        if evt.key() == QtCore.Qt.Key_D:
            self.renderArea.vel.setX(10)
            self.renderArea.vel.setY(0) 
        
        
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    app.exec_()
