from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
import sys

class MapView(QtWidgets.QGraphicsView):

    def __init__(self, parent, window):
        self.window = window
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(10, 10, 800, 800)
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setGeometry(QRect(10, 10, 810, 810))
        self.setObjectName("mapView")
        self.setScene(self.scene)
        self.pen = QtGui.QPen(Qt.green)
        self.brush = QtGui.QBrush(Qt.green)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.window.savePoints:
            self.lastPoint = event.pos()
            self.window.points.append(self.lastPoint)
            square = QRectF(self.lastPoint.x()-10, self.lastPoint.y()-10, 20, 20)
            print square
            self.scene.addRect(square, self.pen, self.brush)
            self.window.logPane.appendPlainText('Added point to ({}, {})'.format(self.lastPoint.x(), self.lastPoint.y()))
class GroundControlStation(QtWidgets.QMainWindow):
    savePoints = False
    points = []
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        QMainWindow.setObjectName("QMainWindow")
        QMainWindow.resize(1050, 900)
        # Bees. Priorities!
        QMainWindow.setWindowIcon(QtGui.QIcon('src-taha/app_ico.png'))
        # QT Designer added this for some reason.
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # Map view where polygons are created and displayed.
        self.mapView = MapView(self.centralwidget, self)
        self.mapView.installEventFilter(self)
        self.setMouseTracking(True)
        # Resets both the polygon on the map and the points saved.
        self.clearDrawingButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearDrawingButton.setGeometry(QRect(830, 70, 200, 50))
        self.clearDrawingButton.setObjectName("clearDrawingButton")
        self.clearDrawingButton.clicked.connect(self.mapView.scene.clear)
        # Currently only drawing convex polygons. The button toggles point saving.
        self.toggleConvexDrawingButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleConvexDrawingButton.setGeometry(QRect(830, 10, 200, 50))
        self.toggleConvexDrawingButton.setObjectName("toggleConvexDrawingButton")
        self.toggleConvexDrawingButton.clicked.connect(self.toggleConvexDrawing)
        # Figured a log pane would be useful, so that I don't need to check Python console.
        self.logPane = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.logPane.setGeometry(QRect(830, 140, 200, 600))
        self.logPane.setObjectName("plainTextEdit")
        self.logPane.setReadOnly(True)
        # May need to reset the logs.
        self.clearLogsButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearLogsButton.setGeometry(QRect(830, 760, 200, 50))
        self.clearLogsButton.setObjectName("clearLogsButton")
        self.clearLogsButton.clicked.connect(self.clearLogsPane)
        # No idea what it does, might check later.
        QMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(QMainWindow)
        self.statusbar.setObjectName("statusbar")
        QMainWindow.setStatusBar(self.statusbar)
        # May add extra functionality once the main tasks are completed.
        self.menubar = QtWidgets.QMenuBar(QMainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1050, 21))
        self.menubar.setObjectName("menubar")
        # TODO: Populate sub-menus here.
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        # TODO: Explain how drawing works, what drawing toggle changes briefly.
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        QMainWindow.setMenuBar(self.menubar)
        # TODO: Add save/load previously generated points feature.
        self.actionOpen_Preset = QtWidgets.QAction(QMainWindow)
        self.actionOpen_Preset.setObjectName("actionOpen_Preset")
        self.actionSave_Preset = QtWidgets.QAction(QMainWindow)
        self.actionSave_Preset.setObjectName("actionSave_Preset")
        self.actionExit = QtWidgets.QAction(QMainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen_Preset)
        self.menuFile.addAction(self.actionSave_Preset)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        # Everything should be ready, inform the operator.
        self.logPane.appendPlainText("Initialized GCS.")
        # Currently no localization, may prove useful later on though.
        self.retranslateUi(QMainWindow)
        # No idea what it does, may check later.
        #QtWidgets.QApplication.processEvents()
        QMetaObject.connectSlotsByName(QMainWindow)

    def retranslateUi(self, QMainWindow):
        # TO-DO: Review this whole translate thing.
        _translate = QCoreApplication.translate
        QMainWindow.setWindowTitle(_translate("QMainWindow", "Ground Control Station"))
        self.clearDrawingButton.setText(_translate("QMainWindow", "Clear Drawing"))
        self.toggleConvexDrawingButton.setText(_translate("QMainWindow", "Enable Convex Drawing"))
        self.clearLogsButton.setText(_translate("QMainWindow", "Clear Logs"))
        self.menuFile.setTitle(_translate("QMainWindow", "File"))
        self.menuHelp.setTitle(_translate("QMainWindow", "Help"))
        self.actionOpen_Preset.setText(_translate("QMainWindow", "Open Preset"))
        self.actionSave_Preset.setText(_translate("QMainWindow", "Save Preset"))
        self.actionExit.setText(_translate("QMainWindow", "Exit"))
    
    def toggleConvexDrawing(self):
        if self.savePoints:
            self.logPane.appendPlainText("Stopped recording points.")
            self.toggleConvexDrawingButton.setText("Enable Convex Drawing")
        else:
            self.logPane.appendPlainText("Started recording points.")
            self.toggleConvexDrawingButton.setText("Disable Convex Drawing")
        self.savePoints = not self.savePoints
    
    def keyPressEvent(self, event):
        print "hmmmmm"
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def eventFilter(self, source, event):
        if (source is self.mapView and event.type() == QEvent.KeyPress):
            # Pass the event to overwritten method on MapView class.
            self.keyPressEvent(event)
        return QtWidgets.QMainWindow.eventFilter(self, source, event)

    def clearLogsPane(self):
        self.logPane.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QMainWindow = QtWidgets.QMainWindow()
    ui = GroundControlStation()
    QMainWindow.show()
    sys.exit(app.exec_())
