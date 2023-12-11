import sys

from PyQt6.QtWidgets import *

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(200, 200)
        self.setWindowTitle("Converter/")

        """self.btn1 = QPushButton("EURO to UAN", self)
        self.btn1.move(15, 50)
        self.result_label = QLabel("Результат в Гривнах:", self)  # Создаем метку для вывода результата

        self.btn2 = QPushButton("UAN to EURO", self)
        self.btn2.move(155, 50)

        self.btn1.clicked.connect(self.evt_btn_clicked())
        self.btn2.clicked.connect(self.evt_btn_clicked())"""

        self.btn = QPushButton("Show message", self)
        self.btn.move(35, 50)
        self.btn.clicked.connect(self.evt_btn_clicked)

    def evt_btn_clicked(self):
        d = 38
        i_amount, b_ok= QInputDialog.getInt(self,\
                                             "Title",\
                                             "This amount will convert both ways",\
                                             0, 0, 100000000, 100)

        #uah = i_amount, "Uan = ", (i_amount / d), "Euro"
        uah = f"{i_amount} Uah = {i_amount / d:.2f} Euro"
        #uah = f"{uah:.2f)}"
        string = str(uah)
        if b_ok:
            QMessageBox.information(self, "Amount", str(i_amount) + "Euro = " + str(i_amount * d) + " Uan\n" + string)
            #QMessageBox.information(self,"Amount", string)

        else:
            QMessageBox.information(self, "Amount", string)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())