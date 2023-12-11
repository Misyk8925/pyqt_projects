import sys
from PyQt6.QtWidgets import *  #QApplication, QDialog, QPushButton, QMessageBox  #import section

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)

        self.btn = QPushButton("Show message", self)
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

    def evt_btn_clicked(self):
        #colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
        i_age, b_ok = QInputDialog.getInt(self, "Title", "Enter your age:", 18, 18, 65, 1)
        #s_color, b_ok = QInputDialog.getItem(self, "Title", "Enter your favourite colour:", colors,) # editable = True

        if b_ok:
            QMessageBox.information(self, "Colour", "Your favourite color is: " + str(i_age))
        else:
            QMessageBox.critical(self, "Canceled", "User have clicked CANCEL")



if __name__ == "__main__":
            app = QApplication(sys.argv)  # create application
            dlgMain = DlgMain()  # create main gui window
            dlgMain.show()  # show gui
            sys.exit(app.exec())  # execude the application