import math
import random
from Ball import *
from Util import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter, QPalette
from PyQt5.QtCore import QPointF, QRectF, Qt, QTimer, QSize, pyqtSignal, QLineF
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit, QApplication, QGraphicsEllipseItem, QGraphicsLineItem


class Arena:

    def __init__(self, scene):
        self.scene = scene
        self.balls = []
        self.offset = 0

    def makeWalls(self):
        self.outerSquare = QRectF(QPointF(-ARENA_SIZE/2-15, -ARENA_SIZE/2-15), QPointF( ARENA_SIZE + 50, ARENA_SIZE+50))
        self.outer = QGraphicsRectItem(self.outerSquare)
        brushBlack = QBrush(Qt.black)
        self.outer.setBrush(brushBlack)
        self.scene.addItem(self.outer)
        #
        self.innerSquare = QRectF(QPointF(-ARENA_SIZE/2, -ARENA_SIZE/2), QPointF( ARENA_SIZE/2, ARENA_SIZE/2))
        self.inner = QGraphicsRectItem(self.innerSquare)
        brushWhite = QBrush(Qt.white)
        self.inner.setBrush(brushWhite)
        self.scene.addItem(self.inner)
        #
        self.frame = QRectF(QPointF(-ARENA_SIZE/2, -ARENA_SIZE/2), QPointF(ARENA_SIZE/2, ARENA_SIZE/2)) 
        self.frameItem = QGraphicsRectItem(self.frame)
        self.scene.addItem(self.frameItem)

    def makeGoal(self):
        aso = ARENA_SIZE/2 + self.offset * 10
        self.goal= QRectF(
            QPointF(-aso, -aso), 
            QPointF(aso, aso))
        self.goalItem = QGraphicsEllipseItem(self.goal) 
        self.scene.addItem(self.goalItem)

    def makeBalls(self):
        for i in range(AMOUNT_OF_BALLS):
            pos = randomPos()
            if not self.anyOverlap(pos):
                continue
            self.balls.append(Ball(self.scene, pos, QPointF(0, 0)))

    
    def anyOverlap(self, pos):
        for ball in self.balls:
            if length(QPointF(ball.pos - pos)) < 2*BALL_RADIUS:
                return False
        return True

    def tick(self):
        # bounce off walls  
        for b in self.balls:
            if b.faded == 0:
                self.bounceOffWalls(b)
        # bounce off other Balls
        for i in range(len(self.balls)):
            for j in range(len(self.balls)):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if b1.faded == 0 and b2.faded == 0 and i != j:
                    self.bounceOffBalls(b1, b2)

        # for r in self.balls:
        for b in self.balls:
            b.tick()

         # checking if a Ball is in goal
        for b in self.balls:
            if length(b.pos) > ARENA_SIZE/2:
                b.setFade()
    
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
        if ((x + BALL_RADIUS) > a and xVel > 0) or ((x - BALL_RADIUS) < -a and xVel < 0):
            xVel = -xVel
        if ((y + BALL_RADIUS) > a and yVel > 0) or ((y - BALL_RADIUS) < -a and yVel < 0):
            yVel = - yVel
        Ball.vel = QPointF(xVel, yVel)

    def tryKey(self, evt):
        ball = None
        for b in self.balls:
            if b.gun != None:
                ball = b
        if ball is not None:
            if self.isStill():
                if evt.key() == Qt.Key_L:
                    ball.gun.addToAngle(0.1)
                if evt.key() == Qt.Key_K:
                    ball.gun.addToAngle(-0.1)
                if evt.key() == Qt.Key_Space:
                    ball.fireGun()

    def tryClick(self, x, y):
        for r in self.balls:
            if length(QPointF(x, y) - r.pos) < 50:
                if r.gun is None:
                    r.attachGun()
                else:
                    r.removeGun()

    def isStill(self):
        totalVel = 0
        for ball in self.balls:
            totalVel += length(ball.vel)
        if totalVel < 7.5:
            return True
        return False
        # self.gun1 = Gun(self.scene, QPointF(0, 280), QPointF(0, 0))