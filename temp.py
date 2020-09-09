import sys
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QTransform, QBrush, QColor, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy, QSpacerItem, QGraphicsObject
 
 
class MouseBrushObject(QGraphicsObject):
    def __init__(self):
        QGraphicsObject.__init__(self)
        self._size = 10
        self._x = 0
        self._y = 0
        self._pen = None
        self._brush = None
        self._color = None
        self.setColor(QColor(255, 0, 0, 255))
 
    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawEllipse(rect)
 
    def boundingRect(self):
        return QRectF(self._x, self._y, self._size, self._size)
 
    def setColor(self, color):
        self._color = color
        self._pen = QPen(self._color, 1)
        self._brush = QBrush(QColor(self._color.red(), self._color.green(), self._color.blue(), 40))
 
    def setSize(self, size):
        self._size = size
 
    def setPosition(self, pos):
        self._x = pos.x()-self._size/2
        self._y = pos.y()-self._size/2
        self.setPos(QPointF(self._x, self._y))
 
 
class View(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.setMouseTracking(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        pixmap = QPixmap(300, 300)
        self.scene.addItem(QGraphicsPixmapItem(pixmap))
        #self.setTransform(QTransform().scale(1, 1).rotate(0))
        self.scene.setBackgroundBrush(QBrush(Qt.lightGray))
        self._brushItem = MouseBrushObject()
 
    def mouseMoveEvent(self, event):
        pos = event.pos()
        #pos = self.mapToScene(pos)
        #pos = self.mapFromScene(pos)
        #pos = self.mapToGlobal(pos)
        #pos = self.mapFromGlobal(self.mapToGlobal(pos))
        #pos = self.mapToGlobal(self.mapFromGlobal(pos))
        #pos = self.mapToGlobal(self.mapFromScene(pos))
        self._brushItem.setPosition(pos)
 
    def enterEvent(self, event):
        self.scene.addItem(self._brushItem)
        return super(View, self).enterEvent(event)
 
    def leaveEvent(self, event):
        self.scene.removeItem(self._brushItem)
        return super(View, self).leaveEvent(event)
 
 
class Viewer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
 
        layout = QVBoxLayout()
        self.view = View(self)
        self.setLayout(layout)
 
        layout.addWidget(self.view)
 
 
class MainWindow(QMainWindow):
 
    def __init__(self):
        QMainWindow.__init__(self)
        self.viewer = Viewer(self)
 
        layout = QVBoxLayout()
        layout.addWidget(self.viewer)
        centralwidget = QWidget(self)
        centralwidget.setLayout(layout)
        self.setCentralWidget(centralwidget)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())