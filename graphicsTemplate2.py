from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QApplication,
                             QGraphicsScene, QGraphicsView)
from PyQt5.QtCore import Qt, pyqtSignal


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
        self.scene = QGraphicsScene()
        self.view = MyView()
        self.view.setScene(self.scene)
        self.scene.setSceneRect(-150, -150, 300, 300)
        lo = QHBoxLayout()
        lo.addWidget(self.view)
        self.setLayout(lo)
        self.setWindowTitle("Ripple")

        
        
        
if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()
