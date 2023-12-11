#first programm
"""
import sys
from PyQt6.QtWidgets import *  #import section

app = QApplication(sys.argv)  #create application

dlgmain = QDialog()  #create main GUI window
dlgmain.setWindowTitle("First GUI")

dlgmain.show()  # This line shows the main window

sys.exit(app.exec())  #execute the app
"""


import sys
from PyQt6.QtWidgets import *  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(300,200)

        self.ledText = QLineEdit("default text",self)  # add text
        self.ledText.move(90, 50)

        self.setWindowTitle("second gui") # add widgets and set properties
        self.btnUpdate = QPushButton("Update window title", self)  # btn это префикс при использовании auto-complete
        self.btnUpdate.move(70,80)
        self.btnUpdate.clicked.connect(self.evt_btn_update_clicked)

    def evt_btn_update_clicked(self):
        self.setWindowTitle(self.ledText.text())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())