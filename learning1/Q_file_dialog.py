import sys
from PyQt6.QtWidgets import *  #QApplication, QDialog, QPushButton, QMessageBox  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)

        self.btn = QPushButton("Open file", self)
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

    def evt_btn_clicked(self):
        res = QFileDialog.getOpenFileName(self, "Open File", "/Users/kovalmykhailo", "JPG File (*.jpg;;PNG File (*.png)")
        print(res)


if __name__ == "__main__":
            app = QApplication(sys.argv)  # create application
            dlgMain = DlgMain()  # create main gui window
            dlgMain.show()  # show gui
            sys.exit(app.exec())  # execude the application