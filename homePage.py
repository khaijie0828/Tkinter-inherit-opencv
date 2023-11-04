#homePage.py
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStackedWidget
from PyQt5.QtCore import QThread, pyqtSignal
from main_UI import Ui_MainPage
import mouseFunction


class CameraThread(QThread):
    update_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.active = True

    def run(self):
        camera = cv2.VideoCapture(0)
        while self.active:
            ret, frame = camera.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                frame = cv2.flip(frame, 1)
                pixmap = mouseFunction.handTrackingFunction(frame)
                self.update_signal.emit(pixmap)
        camera.release()

    def stop(self):
        self.active = False


class homeWindow(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.ui = Ui_MainPage()
        self.ui.setupUi(self)
        self.stacked_widget = stacked_widget

        self.camera_label = QLabel(self)
        self.camera_label.setGeometry(95, 25, 450, 340)

        self.camera_thread = CameraThread()
        self.camera_thread.update_signal.connect(self.update_camera_label)
        self.camera_thread.start()

    def update_camera_label(self, pixmap):
        self.camera_label.setPixmap(pixmap)
        self.camera_label.setScaledContents(True)




if __name__ == '__main__':
    app = QApplication([])

    stacked_widget = QStackedWidget()
    stacked_widget.setFixedSize(640, 480)

    main_page = homeWindow(stacked_widget)

    stacked_widget.addWidget(main_page)

    stacked_widget.setCurrentIndex(0)
    stacked_widget.show()

    app.exec_()
