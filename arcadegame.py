import math
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication, QGraphicsEllipseItem

ARENA_SIZE = 600


class Bullet:
    def __init__(self, scene, pos, vel):
        self.pos = pos
        self.vel = vel
        self.scene = scene
        r = 10
        re = QRectF(QPointF(-r/2, -r/2), QPointF(r/2, r/2))
        self.item = QGraphicsEllipseItem(re)
        self.item.setPos(self.pos)
        self.scene.addItem(self.item)

    def tick(self):
        self.pos += self.vel
        self.item.setPos(self.pos)

class Gun: 
    def __init__(self, scene, pos, vel):
        self.pos = pos
        self.vel = vel
        self.scene = scene
        self.bullets = []
        size = 20
        r = QRectF(QPointF(-size/2, -size/2), QPointF(size/2, size/2))
        self.item = QGraphicsRectItem(r)
        self.item.setPos(self.pos)
        self.scene.addItem(self.item)

    def tick(self):
        x = self.pos.x()
        y = self.pos.y()
        xVel = self.vel.x()
        yVel = self.vel.y()
        a = ARENA_SIZE/2
        if (x > a and xVel > 0) or (x < -a and xVel < 0):
            xVel = -xVel
        if (y > a and yVel > 0) or (y < -a and yVel < 0):
            yVel = - yVel
        self.vel = QPointF(xVel, yVel)
        self.vel *= 0.99
        self.pos += self.vel
        self.item.setPos(self.pos)

    def addBullet(self):
        self.bullets.append(Bullet(self.scene, self.pos + QPointF(0, -10), QPointF(0, -5)))
        

class Rock:
    def __init__(self, scene, pos, vel):
        self.pos = pos
        self.vel = vel
        self.scene = scene
        r = 50
        re = QRectF(QPointF(-r/2, -r/2,), QPointF(r/2, r/2))
        self.item = QGraphicsEllipseItem(re)
        self.item.setPos(self.pos)
        self.scene.addItem(self.item)
    
    def tick(self):
        x = self.pos.x()
        y = self.pos.y()
        xVel = self.vel.x()
        yVel = self.vel.y()
        a = ARENA_SIZE/2
        if (x > a and xVel > 0) or (x < -a and xVel < 0):
            xVel = -xVel
        if (y > a and yVel > 0) or (y < -a and yVel < 0):
            yVel = - yVel
        self.vel = QPointF(xVel, yVel)
        self.pos += self.vel
        self.item.setPos(self.pos)        



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
        self.gview = QGraphicsView()
        self.gview.setScene(self.scene)
        self.gview.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.scene.setSceneRect(
            -ARENA_SIZE/2, -ARENA_SIZE/2,
            ARENA_SIZE, ARENA_SIZE)
        lo.addWidget(self.gview)
        # it = QGraphicsRectItem(QPointF(0, 0), QPointF(100, 100))
        # self.scene.addItem(it)
        self.rock1 = Rock(self.scene, QPointF(0, 0), QPointF(3, 1))
        self.gun1 = Gun(self.scene, QPointF(0, 280), QPointF(0, 0))

    def tick(self):
        self.rock1.tick()
        self.gun1.tick()
        for bullet in self.gun1.bullets:
            bullet.tick()
        # self.scene.addItem(r)
 
    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_D:
            self.gun1.vel = QPointF(10, 0)
        if evt.key() == Qt.Key_A:
            self.gun1.vel = QPointF(-10, 0)
        if evt.key() == Qt.Key_Space:
            self.gun1.addBullet()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    app.exec_()