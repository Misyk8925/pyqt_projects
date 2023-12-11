import sys

from PyQt6.QtCore import QDate, QTime, QDateTime
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *  #QApplication, QDialog, QPushButton, QMessageBox  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)

        self.btn = QPushButton("Show dates", self)
        self.btn.move(35, 50)

        font = QFont("Arial", 14, 75, True)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.evt_btn_clicked)


    def evt_btn_clicked(self):
        dt = QDate.currentDate()
        print(dt.toString())
        print(dt.toJulianDay())
        print(dt.dayOfWeek())
        print(dt.dayOfYear())
        print(dt.addDays(21).toString())

        tm = QTime(13, 20, 25, 335)
        tm2 = QTime(15, 20)
        print(tm.toString())
        print(tm.msec())
        print(tm.secsTo(tm2))

        dtm = QDateTime.currentDateTime()
        print(dtm.toString())

if __name__ == "__main__":
            app = QApplication(sys.argv)  # create application
            dlgMain = DlgMain()  # create main gui window
            dlgMain.show()  # show gui
            sys.exit(app.exec())  # execude the application