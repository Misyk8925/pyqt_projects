import sys
from PyQt6.QtWidgets import *
from random import *
import sqlite3 as sq


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        WIDTH = 200  # set main window
        HIGHT = 350
        self.resize(WIDTH, HIGHT)
        self.setWindowTitle("Words training")

        self.layout = QVBoxLayout(self)  # add vertical layout
        self.german_word = QLabel(" ", self)

        self.db_creation()  # Create database with words

        self.german_list = self.creating_lists_of_words("german_word")  # import from database word into lists
        self.english_list = self.creating_lists_of_words("english_word")

        if len(self.german_list):  # if there is any words
            self.advanced_init_ui()
        else:
            self.display_add_new_word_function()  # if not, display function, that should add new words
            if len(self.german_list):
                self.init_main_window_ui()  # start main window

    def db_creation(self):
        with sq.connect("words_list.db") as self.con:
            self.cur = self.con.cursor()  # return an example of class Cursor
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS words
            (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                german_word TEXT,
                english_word TEXT
            )
            """)

    def creating_lists_of_words(self, column):  # adding new words to lists
        self.cur.execute(f"SELECT {column} FROM words")
        return [word[0] for word in self.cur.fetchall()]

    def adding_new_word(self):
        dialog = InputDialog()  # add new window, where user can add new word
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:  # if dialog window has finished
            user_input = dialog.get_user_input()

            self.cur.execute("INSERT INTO words (german_word, english_word) VALUES (?, ?)", user_input)
            self.con.commit()  # update the database

            self.german_list.append(str(user_input[0]))
            self.english_list.append(user_input[1])

            if len(self.german_list) == 1:
                self.init_main_window_ui()
        else:
            print("Operation has been cancelled")

    def display_add_new_word_function(self):
        self.db_creation()

        aw_label = QLabel("Click below, if you want to add new word")
        self.layout.addWidget(aw_label)
        add_word = QPushButton("Add new word")
        self.layout.addWidget(add_word)
        add_word.clicked.connect(self.adding_new_word)

    def init_main_window_ui(self):
        self.random_number = randint(0, len(self.german_list) - 1)

        print(self.german_list)
        print(self.english_list)

        self.s = self.german_list[self.random_number]  # random word

        self.german_word = QLabel("Word on german:", self)
        self.word = QLabel(self.s)

        english_word_label = QLabel("Word on english: ", self)
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

        """self.btn_edit_word = QPushButton("Edit word")
        self.layout.addWidget(self.btn_edit_word)
        self.btn_edit_word.clicked.connect(self.edit_word)"""

        self.setLayout(self.layout)

    def advanced_init_ui(self):
        self.init_main_window_ui()
        self.display_add_new_word_function()

    def get_result(self):
        answer = str(self.word_input.text())
        print(answer)
        print(self.english_list[self.random_number][2:-3])

        if answer == str(self.english_list[self.random_number]):
            self.result_label.setText("Correct")

        else:
            self.result_label.setText("Incorrect")

    def restart(self):
        self.random_number = randint(0, len(self.german_list) - 1)
        self.s = self.german_list[self.random_number]  # formatted word
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

        german_word_label = QLabel("Word on german: ", self)
        layout.addWidget(german_word_label)

        self.input_field_german = QLineEdit(self)
        layout.addWidget(self.input_field_german)

        english_word_label = QLabel("Word on english: ", self)
        layout.addWidget(english_word_label)

        self.input_field_english = QLineEdit(self)
        layout.addWidget(self.input_field_english)

        # Create a QDialogButtonBox widget containing "OK" and "Cancel" buttons.
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        # Connect the "accepted" signal of the button box to the accept() method of the QDialog.
        # The "accepted" signal is emitted when the "OK" button is clicked.
        buttons.accepted.connect(self.accept)

        # Connect the "rejected" signal of the button box to the reject() method of the QDialog.
        # The "rejected" signal is emitted when the "Cancel" button is clicked.
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setLayout(layout)
        self.setWindowTitle('Dialog window')

    def get_user_input(self):
        self.input_list = [self.input_field_german.text(), self.input_field_english.text()]
        return self.input_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())