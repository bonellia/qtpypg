import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())
    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QtGui.QCursor()
        print(cursor.pos())
    def initUI(self):
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('Quit button')
        self.show()
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()