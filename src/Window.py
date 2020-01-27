
import math
import random
from Ball import *
from Control import *
from Util import *
from Arena import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize, pyqtSignal, QLineF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication, QGraphicsEllipseItem, QGraphicsLineItem



# Window Class
# includes the timer
# instantiate a control, and an arena
#
# arena holds list of all graphics items: Walls, Balls, etc
#
# control class keeps a record of current state

class MyView(QGraphicsView):

    mySignal = pyqtSignal(float, float)
    
    def __init__(self):
        super(MyView, self).__init__()

    def mousePressEvent(self, e):
        pos = self.mapToScene(e.pos())
        self.mySignal.emit(pos.x(), pos.y())

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        lo = QVBoxLayout()
        self.setLayout(lo)
        self.setWindowTitle("Robot Battle")

        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.tick)
        self.timer.start(30)

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMinimumSize(
            QSize(ARENA_SIZE + 50, ARENA_SIZE + 50))

        self.scene = QGraphicsScene()
        self.gview = MyView()
        self.gview.mySignal.connect(self.recieveClick)
        self.gview.setScene(self.scene)
        self.gview.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.scene.setSceneRect(
            -ARENA_SIZE/2, -ARENA_SIZE/2,
            ARENA_SIZE, ARENA_SIZE)
        lo.addWidget(self.gview)
        self.arena = Arena(self.scene)
        self.control = Control(self.arena)
        self.arena.makeWalls()
        self.arena.makeGoal()
        self.arena.makeBalls()

    def bounceOffBalls(self, r1, r2):
        if length(r2.pos - r1.pos) < 100:
            v1_new, v2_new = bouncing(r1.pos, r1.vel, r2.pos, r2.vel)
            r1.vel = v1_new
            r2.vel = v2_new

    def bounceOffWalls(self, Ball):
        x = Ball.pos.x()
        y = Ball.pos.y()
        xVel = Ball.vel.x()
        yVel = Ball.vel.y()
        a = ARENA_SIZE/2
        if ((x + self.radius) > a and xVel > 0) or ((x - self.radius) < -a and xVel < 0):
            xVel = -xVel
        if ((y + self.radius) > a and yVel > 0) or ((y - self.radius) < -a and yVel < 0):
            yVel = - yVel
        Ball.vel = QPointF(xVel, yVel)

    def fireGun(self):
        a = math.pi * self.gun.ang / 180 
        v = 20 * QPointF(math.cos(a), math.sin(a))
        r = Ball(self.scene, QPointF(0, 300), v)
        self.Balls.append(r)

    def tick(self):
        self.control.tick()

    def keyPressEvent(self, evt):
        self.control.keyPressEvent(evt)

    def recieveClick(self, x, y):
        self.control.recieveClick(x, y)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    app.exec_()
