"""import sys
from PyQt6.QtWidgets import *


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        start = 0
        self.resize(400, 400)

        self.setWindowTitle("Calculator")

        layout = QGridLayout()


        self.btn_one = QPushButton("1")
        self.btn_two = QPushButton("2")
        self.btn_three = QPushButton("3")

        self.btn_four = QPushButton("4")
        self.btn_five = QPushButton("5")
        self.btn_six = QPushButton("6")

        self.btn_seven = QPushButton("7")
        self.btn_eight = QPushButton("8")
        self.btn_nine = QPushButton("9")

        self.btn_zero = QPushButton("0")

        layout.addWidget(self.btn_zero, 0, 0)
        layout.addWidget(self.btn_one, 0, 1)
        layout.addWidget(self.btn_two, 0, 2)
        layout.addWidget(self.btn_three, 1, 0)
        layout.addWidget(self.btn_four, 1, 1)
        layout.addWidget(self.btn_five, 1, 2)
        layout.addWidget(self.btn_six, 2, 0)
        layout.addWidget(self.btn_seven, 2, 1)
        layout.addWidget(self.btn_eight, 2, 2)
        layout.addWidget(self.btn_nine, 3, 0)

        self.btn_zero.clicked.connect(self,zeros)
        self.btn_one.clicked.connect(self, first)


        def zeros(self):
            a = 0
            res = start * 10 + a
            return res

        def first(self):
            a = 1
            res = start * 10 + a
            return a
        self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())"""


import sys
from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QPushButton

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("Calculator")

        layout = QGridLayout()
        self.setLayout(layout)

        buttons = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "0"
        ]

        self.start = 0

        for i, label in enumerate(buttons):
            button = QPushButton(label)
            layout.addWidget(button, i // 3, i % 3)
            button.clicked.connect(lambda ch=label: self.on_button_click(ch))

    def on_button_click(self, char):
        if char.isdigit():
            self.start = self.start * 10 + int(char)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())
