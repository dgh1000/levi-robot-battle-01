import math
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication
# from Robot import Robot
# import Util
# from Arena import Arena

class Shell():
    def __init__(self, scene, pos, vel, other):
        self.scene = scene
        self.pos = pos
        self.vel = vel
        rect = QRectF(QPointF(-5, -5), QPointF(5, 5))
        self.item = QGraphicsRectItem(rect)
        self.item.setPos(pos)
        self.other = other
        scene.addItem(self.item)

    def tick(self):
        self.pos += self.vel
        self.item.setPos(self.pos)
        if self.scene.collidingItems(self.other):
            print("You win!")

    
    def isInside(self):
        return (0 < self.pos.x < 400 and 0 < self.pos.y < 400)


class Roomba():
    def __init__(self, scene, pos, vel, dir):
        self.scene = scene
        self.pos = pos
        self.vel = vel
        self.dir = dir
        rect = QRectF(QPointF(-10, -10), QPointF(10, 10))
        self.shells = []
        self.item = QGraphicsRectItem(rect)
        self.item.setPos(pos)
        scene.addItem(self.item)

    def tick(self):
        self.vel = self.vel * 0.95
        self.pos += (self.vel)
        self.item.setPos(self.pos)

    def setOther(self, other):
        self.other = other

    def addShell(self):
        self.shells.append(Shell(self.scene, self.pos + QPointF(2*self.dir.x(), 0),
                                 self.dir, self.other))



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.arenaSize = 600
        lo = QVBoxLayout()
        self.setLayout(lo)
        self.setWindowTitle("Robot Battle")

        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.timeUpdate)
        self.timer.start(30)

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMinimumSize(
            QSize(self.arenaSize + 100, self.arenaSize + 250))

        self.scene = QGraphicsScene()
        self.gview = QGraphicsView()
        self.gview.setScene(self.scene)
        self.gview.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # add label widget
        displayWidget = QTextEdit('n/a', self)
        lo.addWidget(displayWidget)

        self.scene.setSceneRect(
            -self.arenaSize/2, -self.arenaSize/2,
            self.arenaSize, self.arenaSize)
        lo.addWidget(self.gview)


        self.roomba1 = Roomba(self.scene, QPointF(-200, 0), QPointF(0, 0), QPointF(10, 0))
        self.roomba2 = Roomba(self.scene, QPointF(200, 0), QPointF(0, 0), QPointF(-10, 0))
        self.roomba1.setOther(self.roomba2.item)
        self.roomba2.setOther(self.roomba1.item)
        # r = QGraphicsRectItem(QRectF(QPointF(-100, -100), QPointF(100, 100)))
        # self.scene.addItem(r)
        

    def timeUpdate(self):
        self.roomba1.tick()
        self.roomba2.tick()
        for shell in self.roomba1.shells:
            shell.tick()
            if not shell.isInside:
                shell.scene.removeItem(shell.item)
        
        for shell in self.roomba2.shells:
            shell.tick()
            if not shell.isInside:
                shell.scene.removeItem(shell.item)
        # for shell in self.roomba2.shells:
        #     shell.tick()
        # for o in self.robots:
        #     o.tick()
        # report = self.arena.detectCollisions()
        # for this, others in report:
        #     print(this.name, [o.name for o in others])
        # print('--')

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_W:
            self.roomba1.vel = QPointF(0, -10)
        if evt.key() == Qt.Key_S:
            self.roomba1.vel = QPointF(0, 10)
        if evt.key() == Qt.Key_D:
            self.roomba1.addShell()
        if evt.key() == Qt.Key_I:
            self.roomba2.vel = QPointF(0, -10)
        if evt.key() == Qt.Key_K:
            self.roomba2.vel = QPointF(0, 10)
        if evt.key() == Qt.Key_J:
            self.roomba2.addShell()
        
if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()