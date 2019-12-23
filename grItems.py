import math
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QBrush, QPen, QPolygonF, QPainter
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsScene, QGraphicsView, \
    QHBoxLayout, QWidget, QGraphicsRectItem, QLabel, QVBoxLayout, QTextEdit
from Robot import Robot
import Util
from Arena import Arena

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
        self.timer.start(100)

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

    def timeUpdate(self):
        pass
        # for o in self.robots:
        #     o.tick()
        # report = self.arena.detectCollisions()
        # for this, others in report:
        #     print(this.name, [o.name for o in others])
        # print('--')
