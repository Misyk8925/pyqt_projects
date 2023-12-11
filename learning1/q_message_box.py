import sys
from PyQt6.QtWidgets import *  #QApplication, QDialog, QPushButton, QMessageBox  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)

        self.btn = QPushButton("Show message",self)
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

    def evt_btn_clicked(self):
        """res = QMessageBox.question(self, "Disk full", "Your hard disk is almost full")
        if res == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "", "You have clicked YES button")
        elif res == QMessageBox.StandardButton.No:
            QMessageBox.information(self, "", "You have clicked NO button")"""
        msgDiskFull = QMessageBox()
        msgDiskFull.setText("Your hard disk is almost full")
        msgDiskFull.setDetailedText("Please free up disk space")
        msgDiskFull.setIcon(QMessageBox.Icon.Information)
        msgDiskFull.setWindowTitle("Full drive")
        msgDiskFull.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msgDiskFull.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)  #create application
    dlgMain = DlgMain()  #create main gui window
    dlgMain.show()  #show gui
    sys.exit(app.exec())  #execude the application