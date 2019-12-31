import math
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize, pyqtSignal, QLineF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication, QGraphicsEllipseItem, QGraphicsLineItem

ARENA_SIZE = 600



def length(a):
    return math.sqrt(a.x() * a.x() + a.y() * a.y() )

def component(a, b):
    "component of a in the direction of b"
    dp = dotProduct(a, b)   
    return dp * b / (length(b) ** 2)

def dotProduct(a, b):
    return a.x() * b.x() + a.y() * b.y()

def bouncing(p1, v1, p2, v2):
    l1 = p2 - p1
    l2 = p1 - p2
    v1_p = component(v1, l1)
    v1_o = v1 - v1_p
    v2_p = component(v2, l2)
    v2_o = v2 - v2_p
    v1_new = v2_p + v1_o
    v2_new = v1_p + v2_o
    if dotProduct(v1_p - v2_p, l1) < 0:
        return v1, v2
    return v1_new, v2_new
   


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
        self.item.setRotation(180 * self.ang / (2 * math.pi))

    def setPos(self, newPos):
        self.pos = newPos
        self.item.setPos(self.pos)

    def deleteGun(self):
        self.scene.removeItem(self.item)



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



class MyView(QGraphicsView):

    mySignal = pyqtSignal(float, float)
    
    def __init__(self):
        super(MyView, self).__init__()

    def mousePressEvent(self, e):
        pos = self.mapToScene(e.pos())
        self.mySignal.emit(pos.x(), pos.y())

class Rock:
    def __init__(self, scene, pos, vel):
        self.pos = pos
        self.vel = vel
        self.scene = scene
        r = 100
        re = QRectF(QPointF(-r/2, -r/2,), QPointF(r/2, r/2))
        self.item = QGraphicsEllipseItem(re)
        self.item.setPos(self.pos)
        self.scene.addItem(self.item)
        self.gun = None
    
    def tick(self):
        self.vel = self.vel * .99
        self.pos += self.vel
        if self.gun:
            self.gun.setPos(self.pos)
        self.item.setPos(self.pos)        

    def attachGun(self):
        self.gun = Gun(self.scene, self.pos)

    def removeGun(self):
        self.gun.deleteGun()
        self.gun = None

    def fireGun(self):
        if self.gun is not None:
            uv = QPointF(math.cos(self.gun.ang), math.sin(self.gun.ang)) * 5
            self.vel += uv
        
    def remove(self):
        self.removeGun()
        self.scene.removeItem(self.item)


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
        # it = QGraphicsRectItem(QPointF(0, 0), QPointF(100, 100))
        # self.scene.addItem(it)
        self.rock1 = Rock(self.scene, QPointF(0, 0), QPointF(-10, 0))
        # self.rock2 = Rock(self.scene, QPointF(0, 50), QPointF(-5, 0))
        # self.rock3 = Rock(self.scene, QPointF(100, 0), QPointF(3, 0))
        # self.rock4 = Rock(self.scene, QPointF(-200, 30), QPointF(0, 2))
        self.rocks = [self.rock1]
        self.goal1= QPolygonF([QPointF(-350, -350), QPointF(-350, -100), QPointF(-100, -350)])
        self.goalItem1 = QGraphicsPolygonItem(self.goal1) 
        self.scene.addItem(self.goalItem1)
        self.goals = [self.goal1]
        # self.gun1 = Gun(self.scene, QPointF(0, 280), QPointF(0, 0))


    def bounceOffRocks(self, r1, r2):
        if length(r2.pos - r1.pos) < 100:
            v1_new, v2_new = bouncing(r1.pos, r1.vel, r2.pos, r2.vel)
            r1.vel = v1_new
            r2.vel = v2_new

    def bounceOffWalls(self, rock):
        x = rock.pos.x()
        y = rock.pos.y()
        xVel = rock.vel.x()
        yVel = rock.vel.y()
        a = ARENA_SIZE/2
        if (x > a and xVel > 0) or (x < -a and xVel < 0):
            xVel = -xVel
        if (y > a and yVel > 0) or (y < -a and yVel < 0):
            yVel = - yVel
        rock.vel = QPointF(xVel, yVel)

    def fireGun(self):
        a = math.pi * self.gun.ang / 180 
        v = 10 * QPointF(math.cos(a), math.sin(a))
        r = Rock(self.scene, QPointF(0, 300), v)
        self.rocks.append(r)

    def tick(self):
        # bounce off walls  
        for r in self.rocks:
            self.bounceOffWalls(r)
        # bounce off other rocks
        for i in range(len(self.rocks)):
            for j in range(len(self.rocks)):
                if i != j:
                    self.bounceOffRocks(self.rocks[i], self.rocks[j])
        # checking if a rock is in goal
        for r in self.rocks:
            for g in self.goals:
                if g.containsPoint(r.pos, 1):
                    self.goals.remove(g)
                    r.remove()

        # for r in self.rocks:
        for r in self.rocks:
            r.tick()
        

    def keyPressEvent(self, evt):
        rock = None
        for r in self.rocks:
            if r.gun != None:
                rock = r
        if rock is not None:
            if evt.key() == Qt.Key_L:
                rock.gun.addToAngle(0.1)
            if evt.key() == Qt.Key_K:
                rock.gun.addToAngle(-0.1)
            if evt.key() == Qt.Key_Space:
                rock.fireGun()


    def recieveClick(self, x, y):
        for r in self.rocks:
            if length(QPointF(x, y) - r.pos) < 50:
                if r.gun is None:
                    r.attachGun()
                else:
                    r.removeGun()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Window()
    win.show()
    app.exec_()