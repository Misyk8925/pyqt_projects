import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *  #QApplication, QDialog, QPushButton, QMessageBox  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)

        self.btn = QPushButton("Choose font", self)
        self.btn.move(35, 50)

        font = QFont("Arial", 14, 75, True)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.evt_btn_clicked)


    def evt_btn_clicked(self):
        font, bOk = QFontDialog.getFont()
        print(font, bOk)
        if bOk:
            print(font.family)
            print(font.pointSize)
            self.btn.setFont(font)


if __name__ == "__main__":
            app = QApplication(sys.argv)  # create application
            dlgMain = DlgMain()  # create main gui window
            dlgMain.show()  # show gui
            sys.exit(app.exec())  # execude the application