from Util import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize, pyqtSignal, QLineF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication, QGraphicsEllipseItem, QGraphicsLineItem
# Ball class,
#

class Gun:
    def __init__(self, scene, pos):
        self.scene = scene
        self.pos = pos
        # self.item = QGraphicsRectItem(
        #     QRectF(
        #         QPointF(-10, -10),
        #         QPointF(10, 10)
        # )   )
        self.item = QGraphicsLineItem(
            QLineF(QPointF(-30, 0), QPointF(30, 0)))
        self.item2 = QGraphicsLineItem(
            QLineF(QPointF(20, -10), QPointF(30, 0)), self.item
        )
        self.item3 = QGraphicsLineItem(
            QLineF(QPointF(20, 10),  QPointF(30, 0)), self.item
        )
        self.ang = 0
        self.scene.addItem(self.item)
        self.item.setPos(self.pos)
        # self.item.setRotation(self.ang)
        pen = QPen(Qt.black)
        pen.setWidth(3)
        self.item.setPen(pen)
        self.item2.setPen(pen)
        self.item3.setPen(pen)
        
    def addToAngle(self, delta):
        self.ang += delta
        self.item.setRotation(180 * self.ang / (math.pi))

    def setPos(self, newPos):
        self.pos = newPos
        self.item.setPos(self.pos)

    def remove(self):
        self.scene.removeItem(self.item)


class Ball:
    def __init__(self, scene, pos, vel):
        self.pos = pos
        self.vel = vel
        self.scene = scene
        re = QRectF(QPointF(-BALL_RADIUS, -BALL_RADIUS,), QPointF(BALL_RADIUS, BALL_RADIUS))
        self.item = QGraphicsEllipseItem(re)
        self.item.setPos(self.pos)
        self.scene.addItem(self.item)
        self.gun = None
        # faded goes from 0 to 100
        self.faded = 0
    
    def tick(self):
        self.vel = self.vel * 0.99
        self.pos += self.vel
        if self.gun:
            self.gun.setPos(self.pos)
        self.item.setPos(self.pos) 
        self.item.setOpacity(1.0 - self.faded/15)

    def setFade(self):
        if self.faded == 0:
            self.removeGun()
            self.faded = 1
        else:
            self.faded += 1

    def isFaded(self):
        return self.faded >= 15
        

    def attachGun(self):
        self.gun = Gun(self.scene, self.pos)

    def removeGun(self):
        if self.gun is not None:
            self.gun.remove()
        self.gun = None

    def fireGun(self):
        if self.gun is not None:
            uv = QPointF(math.cos(self.gun.ang), math.sin(self.gun.ang)) * 10
            self.vel = uv
        
    def remove(self):
        self.removeGun()
        self.scene.removeItem(self.item)