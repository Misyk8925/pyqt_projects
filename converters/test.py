import sys
from PyQt6.QtWidgets import *
from random import *

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(200, 300)
        self.setWindowTitle("Words training")

        layout = QVBoxLayout(self)

        self.english_words = open("/Users/kovalmykhailo/myenvs/myenv/pyqt_projects/words_training/engl.txt")
        self.german_words = open("/Users/kovalmykhailo/myenvs/myenv/pyqt_projects/words_training/grmn.txt")

        self.res_german = [str(word)[:-1] for word in self.german_words]
        self.res_english = [str(word)[:-1] for word in self.english_words]

        self.zufaellige_zahl = randint(0, len(self.res_german) - 1)

        self.german_word = QLabel(f"Word on German: {self.res_german[self.zufaellige_zahl]}", self)
        self.english_word_label = QLabel("Word on English: ", self)
        self.word_input = QLineEdit(self)
        self.result_label = QLabel("Result: ", self)

        layout.addWidget(self.german_word)
        layout.addWidget(self.english_word_label)
        layout.addWidget(self.word_input)
        layout.addWidget(self.result_label)

        self.get_res = QPushButton("Check")
        layout.addWidget(self.get_res)
        self.get_res.clicked.connect(self.get_result)

        self.restart_button = QPushButton("Next word")
        layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.restart)

        self.setLayout(layout)

    def get_result(self):
        answer = str(self.word_input.text())

        if answer == self.res_english[self.zufaellige_zahl]:
            self.result_label.setText("Correct")
        else:
            self.result_label.setText("Incorrect")

    def restart(self):
        self.zufaellige_zahl = randint(0, len(self.res_german) - 1)
        self.german_word.setText(f"Word on German: {self.res_german[self.zufaellige_zahl]}")
        self.word_input.clear()
        self.result_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())