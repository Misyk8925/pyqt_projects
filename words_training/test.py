import sys
from PyQt6.QtWidgets import *
from random import *
import sqlite3 as sq

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()

        WIDTH, HEIGHT = 200, 350
        self.resize(WIDTH, HEIGHT)
        self.setWindowTitle("Words training")

        self.layout = QVBoxLayout(self)
        self.db_creation()

        # Fetch German and English words from the database
        self.german_list = self.fetch_words("german_word")
        self.english_list = self.fetch_words("english_word")
        self.count = 0

        # Initialize main window UI
        if len(self.german_list):
            self.init_main_window_ui()
        else:
            self.display_add_word_option()

    def db_creation(self):
        with sq.connect("words_list.db") as self.con:
            self.cur = self.con.cursor()
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS words2 
                (
                    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    german_word TEXT,
                    english_word TEXT
                )
            """)

    def fetch_words(self, column):
        self.cur.execute(f"SELECT {column} FROM words")
        return [word[0] for word in self.cur.fetchall()]

    def display_add_word_option(self):
        self.db_creation()

        aw_label = QLabel("Click below if you want to add a new word")
        self.layout.addWidget(aw_label)

        add_word = QPushButton("Add new word")
        self.layout.addWidget(add_word)
        add_word.clicked.connect(self.adding_new_word)

        self.init_main_window_ui()

    def adding_new_word(self):
        dialog = InputDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            user_input = dialog.get_user_input()

            self.cur.execute("INSERT INTO words (german_word, english_word) VALUES (?, ?)", user_input)
            self.con.commit()

            self.count += 1
            self.german_list.append(str(user_input[0]))
            self.english_list.append(user_input[1])

            self.restart()
        else:
            print("Operation has been cancelled")

    def init_main_window_ui(self):
        self.random_number = randint(0, len(self.german_list) - 1)
        self.s = self.german_list[self.random_number]

        self.german_word = QLabel("Word on German:", self)
        self.word = QLabel(self.s)

        english_word_label = QLabel("Word on English: ", self)
        self.word_input = QLineEdit(self)
        self.result_label = QLabel("Result: ", self)

        self.layout.addWidget(self.german_word)
        self.layout.addWidget(self.word)
        self.layout.addWidget(english_word_label)
        self.layout.addWidget(self.word_input)
        self.layout.addWidget(self.result_label)

        get_res = QPushButton("Check")
        self.layout.addWidget(get_res)
        get_res.clicked.connect(self.get_result)

        self.btn_restart = QPushButton("Next word")
        self.layout.addWidget(self.btn_restart)
        self.btn_restart.clicked.connect(self.restart)

        aw_label = QLabel("Click below if you want to add a new word")
        self.layout.addWidget(aw_label)

        add_word = QPushButton("Add new word")
        self.layout.addWidget(add_word)
        add_word.clicked.connect(self.adding_new_word)

        self.setLayout(self.layout)

    def get_result(self):
        answer = str(self.word_input.text())
        print(answer)
        print(self.english_list[self.random_number])

        if answer == str(self.english_list[self.random_number]):
            self.result_label.setText("Correct")
        else:
            self.result_label.setText("Incorrect")

    def restart(self):
        self.random_number = randint(0, len(self.german_list) - 1)
        self.s = self.german_list[self.random_number]
        self.german_word.setText("Word on German:")
        self.word.setText(self.s)
        self.word_input.clear()
        self.result_label.clear()

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        warning = QLabel("Be careful not to make a mistake!", self)
        layout.addWidget(warning)

        german_word_label = QLabel("Word on German: ", self)
        layout.addWidget(german_word_label)

        self.input_field_german = QLineEdit(self)
        layout.addWidget(self.input_field_german)

        english_word_label = QLabel("Word on English: ", self)
        layout.addWidget(english_word_label)

        self.input_field_english = QLineEdit(self)
        layout.addWidget(self.input_field_english)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)
        self.setWindowTitle('Dialog window')

    def get_user_input(self):
        return [self.input_field_german.text(), self.input_field_english.text()]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())
