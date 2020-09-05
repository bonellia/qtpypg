import sys

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QPushButton, QVBoxLayout, QWidget, QSlider)

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class CWidget(QWidget):

    def __init__(self):

        super().__init__()

        formbox = QHBoxLayout()
 
        left = QVBoxLayout()
        right = QVBoxLayout()

        gb = QGroupBox('asd')
        left.addWidget(gb)

        grid = QGridLayout()
        gb.setLayout(grid)

        label = QLabel('asd')
        grid.addWidget(label, 1, 0)

        self.pencolor = QColor(0, 0, 0)
        self.penbtn = QPushButton()
        self.penbtn.setStyleSheet('background-color: rgb(0,0,0)')
        self.penbtn.clicked.connect(self.showColorDlg)
        grid.addWidget(self.penbtn, 1, 1)


        label = QLabel('asd')
        grid.addWidget(label, 2, 0)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(3)
        self.slider.setMaximum(21)
        self.slider.setValue(5)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        grid.addWidget(self.slider)

        gb = QGroupBox('asd')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        self.checkbox = QCheckBox('asd')
        self.checkbox.stateChanged.connect(self.checkClicked)
        hbox.addWidget(self.checkbox)

        left.addStretch(1)

        self.view = CView(self)
        right.addWidget(self.view)

        formbox.addLayout(left)
        formbox.addLayout(right)

        formbox.setStretchFactor(left, 0)
        formbox.setStretchFactor(right, 1)

        self.setGeometry(100, 100, 800, 500)

    def checkClicked(self, state):
        self.view.stretch(state)

    def createExampleGroup(self):
        groupBox = QGroupBox("Slider Example")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)

        vbox = QVBoxLayout()
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def showColorDlg(self):

        color = QColorDialog.getColor()

        sender = self.sender()


        self.pencolor = color
        self.penbtn.setStyleSheet('background-color: {}'.format(color.name()))


# QGraphicsView display QGraphicsScene
class CView(QGraphicsView):

    def __init__(self, parent):

        super().__init__(parent)
        self.scene = QGraphicsScene()

        self.setScene(self.scene)

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        self.backgroundImage = None
        self.graphicsPixmapItem = None

        self.setRenderHint(QPainter.HighQualityAntialiasing)

        self.open()

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)

        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):

        # e.buttons()
        if e.buttons() & Qt.LeftButton:

            self.end = e.pos()

            if self.parent().checkbox.isChecked():
                pen = QPen(QColor(255, 255, 255), 10)
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)
                self.start = e.pos()
                return None

            pen = QPen(self.parent().pencolor, self.parent().slider.value())

            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path, pen)

            self.start = e.pos()

    def stretch(self, state):
        self._set_image(state == 2)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath(), filter='Images (*.png *.xpm *.jpg)')
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.backgroundImage = fileName

            self._set_image(False)



    def _set_image(self, stretch: bool):
        tempImg = QPixmap(self.backgroundImage)

        if stretch:
            tempImg = tempImg.scaled(self.scene.width(), self.scene.height())

        if self.graphicsPixmapItem is not None:
            self.scene.removeItem(self.graphicsPixmapItem)

        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.scene.addItem(self.graphicsPixmapItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    w.show()
    sys.exit(app.exec_())