from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome as qta


class Ui_MainPage(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setStyleSheet("background-color: #FFED8E")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        buttonStyle = """   
                        QPushButton {
                            background-color: transparent; 
                            color: #65686B;
                            border: none; 
                            font: bold 20px;
                            border-radius: 5px;
                        }
                        QPushButton:hover {
                            background-color: rgb(250, 130, 49);
                            color: white;
                        }
                        """

        self.settingBtn = QtWidgets.QPushButton(self.centralwidget)
        self.settingBtn.setGeometry(QtCore.QRect(85, 380, 161, 61))
        self.settingBtn.setObjectName("settingBtn")
        self.settingBtn.setStyleSheet(buttonStyle)

        self.tutorialBtn = QtWidgets.QPushButton(self.centralwidget)
        self.tutorialBtn.setGeometry(QtCore.QRect(390, 380, 161, 61))
        self.tutorialBtn.setObjectName("tutorialBtn")
        self.tutorialBtn.setStyleSheet(buttonStyle)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        iconSize = QtCore.QSize(35, 35)
        settingsIcon = qta.icon('fa.cog')
        tutorialIcon = qta.icon('fa.graduation-cap')
        buttonPointer = QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        MainWindow.setWindowTitle("MainWindow")

        self.settingBtn.setIcon(settingsIcon)
        self.settingBtn.setIconSize(iconSize)
        self.settingBtn.setText(" Settings")
        self.settingBtn.setCursor(buttonPointer)

        self.tutorialBtn.setIcon(tutorialIcon)
        self.tutorialBtn.setIconSize(iconSize)
        self.tutorialBtn.setText(" Tutorial")
        self.tutorialBtn.setCursor(buttonPointer)
