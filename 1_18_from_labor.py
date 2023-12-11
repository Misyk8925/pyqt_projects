import sys
from PyQt6.QtWidgets import *

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 200)
        self.setWindowTitle("1_18")

        layout = QVBoxLayout()

        self.result_label = QLabel("Result", self)

        self.megabytes = QLabel("Dateigröße [MB]: ")
        self.m_input = QLineEdit(self)

        self.speed = QLabel("Intenetgeschwindigkeit [Mbit/s]: ")
        self.s_input = QLineEdit(self)

        self.result_label = QLabel("Result: ")

        self.get_result = QPushButton("Calculate")

        layout.addWidget(self.megabytes)
        layout.addWidget(self.m_input)

        layout.addWidget(self.speed)
        layout.addWidget(self.s_input)

        layout.addWidget(self.get_result)
        layout.addWidget(self.result_label)

        self.get_result.clicked.connect(self.calc_result)

        self.setLayout(layout)

    def calc_result(self):
            mb = int(self.m_input.text())
            sp = int(self.s_input.text())

            geschwindigkeit_in_mb = sp / 8
            dauert_in_sec = mb / geschwindigkeit_in_mb

            h = int(dauert_in_sec // 3600)
            m = int(dauert_in_sec // 60 % 60)
            s = int(dauert_in_sec % 60)
            ms = int((dauert_in_sec - int(dauert_in_sec)) * 1000)

            self.result_label.setText(f"Result: {h}h {m}min {s}s {ms}ms")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())