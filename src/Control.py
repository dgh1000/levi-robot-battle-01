from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

class Control:
    def __init__(self, arena):
        self.arena = arena

    def tick(self):
        self.arena.tick()

    def keyPressEvent(self, evt):
        self.arena.tryKey(evt)


    def recieveClick(self, x, y):
        self.arena.tryClick(x, y)
        
