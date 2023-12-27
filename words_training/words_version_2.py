import sys
from PyQt6.QtWidgets import *
from random import *
import sqlite3 as sq


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        """WIDTH = 300
        HIGHT = 700
        self.resize(WIDTH, HIGHT)"""
        self.setWindowTitle("Words training")

        self.layout = QVBoxLayout(self)     # add vertical layout
        self.german_word = QLabel(" ", self)

        self.db_creation()      # Create database with words

        self.german_list = self.creating_lists_of_words("german_word")      # import from database word into lists
        self.english_list = self.creating_lists_of_words("english_word")

        if len(self.german_list):       # if there is any words
            self.advanced_init_ui()     # if not, display function, that should add new words
        else:
            self.display_add_new_word_function()
            if len(self.german_list):
                self.init_main_window_ui()      # start main window

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

    def creating_lists_of_words(self, column):      # adding new words to lists
        self.cur.execute(f"SELECT {column} FROM words")
        return [word[0] for word in self.cur.fetchall()]

    def adding_new_word(self):
        dialog = InputDialog()      # add new window, where user can add new word
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:       # if dialog window has finished
            user_input = dialog.get_user_input()

            self.cur.execute("INSERT INTO words (german_word, english_word) VALUES (?, ?)", user_input)
            self.con.commit()       # update the database

            self.german_list.append(str(user_input[0]))
            self.english_list.append(user_input[1])

            if len(self.german_list) == 1:
                self.init_main_window_ui()

            elif len(self.german_list) > 1:
                self.restart()
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

        btn_get_res = QPushButton("Check")
        self.layout.addWidget(btn_get_res)
        btn_get_res.clicked.connect(self.get_result)

        self.btn_restart = QPushButton("Next word")
        self.layout.addWidget(self.btn_restart)
        self.btn_restart.clicked.connect(self.restart)

        self.init_output_word_list()

        self.btn_open_editor = QPushButton("Edit this word pair")
        self.btn_open_editor.clicked.connect(self.show_editor_window)

        self.layout.addWidget(self.btn_open_editor)

        self.init_deleting_word_list()

        self.btn_open_delete_window = QPushButton("Delete this word pair")
        self.btn_open_delete_window.clicked.connect(self.delete_word_pair)
        self.layout.addWidget(self.btn_open_delete_window)


        self.setLayout(self.layout)

    def advanced_init_ui(self):
        self.init_main_window_ui()
        self.display_add_new_word_function()

    def init_output_word_list(self):
        self.edit_word_label = QLabel("If you want to EDIT any word, please select one from the list below")
        self.layout.addWidget(self.edit_word_label)

        self.words_list = QComboBox(self)
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word
        print(type(self.words_list))
        self.layout.addWidget(self.words_list)

    def init_deleting_word_list(self):
        self.delete_word_label = QLabel("If you want to DELETE any word pair, please select one from the list below")
        self.layout.addWidget(self.delete_word_label)

        self.delete_words_list = QComboBox(self)
        self.fetch_data_from_database()
        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        self.layout.addWidget(self.delete_words_list)

    """def apply_changes(self):
        new_german = self.new_german_word_input.text()
        new_english = self.new_english_word_input.text()

        # Use placeholders to avoid SQL injection
        edit_grmn = "UPDATE words SET german_word = ? WHERE german_word = ?"
        edit_engl = "UPDATE words SET english_word = ? WHERE english_word = ?"

        # Extracting the word from the result
        old_word = str(self.result).split(' ')[0]

        try:
            # Open a new connection within the 'with' statement
            with sq.connect("words_list.db") as con:
                cur = con.cursor()
                cur.execute(edit_grmn, (new_german, old_word))
                cur.execute(edit_engl, (new_english, old_word))
                con.commit()
        except sq.Error as e:
            print(f"Error applying changes: {e}")
        finally:
            self.cur.close()
            self.con.close()

        # Close the dialog after applying changes
        self.accept()"""

    def fetch_data_from_database(self):
        try:
            with sq.connect("words_list.db") as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT german_word FROM words")
                german_data = cursor.fetchall()

                cursor.execute("SELECT english_word FROM words")
                english_data = cursor.fetchall()

                # Using zip to combine corresponding elements from german_data and english_data
                self.word_pairs = list(zip(german_data, english_data))

        except sq.Error as e:
            print(f"Database error: {e}")

    def updating_corrections(self):
        user_corrections_input = self.corrections_dialog.get_corrections_user_input()

        old_word = str(self.selected_item).split('   ')
        print(old_word)
        print((user_corrections_input[0], old_word[0]))
        print((user_corrections_input[1], old_word[2]))
        self.cur.execute("UPDATE words SET german_word = ? WHERE german_word = ?",
                         (user_corrections_input[0], old_word[0]))

        self.cur.execute("UPDATE words SET english_word = ? WHERE english_word = ?",
                         (user_corrections_input[1], old_word[2]))
        self.con.commit()
        a = self.cur.fetchall()
        print(a)

    def get_result(self):
        answer = str(self.word_input.text())
        print(answer)
        print(self.english_list[self.random_number][2:-3])

        if answer == str(self.english_list[self.random_number]):
            self.result_label.setText("Correct")

        else:
            self.result_label.setText("Incorrect")

    def show_editor_window(self):
        # Создаем и отображаем диалоговое окно при выборе элемента из выпадающего списка
        self.selected_item = self.words_list.currentText()
        print(self.selected_item)

        self.corrections_dialog = EditorDialog(str(self.selected_item), self.cur, self.con, parent=self)

        # Use the result of the first exec() call
        if self.corrections_dialog.exec() == QDialog.DialogCode.Accepted:

            self.updating_corrections()
            # Update the UI or perform other actions as needed
        else:
            print("Operation has been cancelled")

        self.restart()

    def delete_word_pair(self):
        delete_selected_item = self.delete_words_list.currentText()
        selected_word_pair = str(delete_selected_item).split("   ")

        # Use a QMessageBox for confirmation
        reply = QMessageBox.question(self, 'Warning',
                                     f"Do you really want to delete the word pair:  {selected_word_pair[0]} - {selected_word_pair[2]}",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.cur.execute("DELETE FROM words WHERE german_word = ? AND english_word = ?",
                             (selected_word_pair[0], selected_word_pair[2]))

            self.con.commit()
            QMessageBox.information(self, "Title", "You have just deleted the selected word pair")
            self.restart()
        else:
            QMessageBox.critical(self, "Canceled", "User clicked CANCEL")



    def restart(self):
        self.random_number = randint(0, len(self.german_list) - 1)
        self.s = self.german_list[self.random_number]  # formatted word
        self.german_word.setText("Word on German:")
        self.word.setText(self.s)
        self.word_input.clear()
        self.result_label.clear()

        self.words_list.clear()
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]} - {str(word_pair[1])[2:-3]}")  # formatted word


        self.delete_words_list.clear()
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")


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


class EditorDialog(QDialog):
    def __init__(self, result, cur, con, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit mode")
        self.cur = cur
        self.con = con
        self.init_window()

    def init_window(self):
        self.correct_german_word = QLabel("Input below new German word:")
        self.correct_german_word_input = QLineEdit(self)

        self.correct_english_word = QLabel("Input below new English word:")
        self.correct_english_word_input = QLineEdit(self)

        self.editor_layout = QVBoxLayout(self)
        self.editor_layout.addWidget(self.correct_german_word)
        self.editor_layout.addWidget(self.correct_german_word_input)
        self.editor_layout.addWidget(self.correct_english_word)
        self.editor_layout.addWidget(self.correct_english_word_input)


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

        self.editor_layout.addWidget(buttons)

        self.setLayout(self.editor_layout)


    def get_corrections_user_input(self):
        self.correct_word_pair_list = [self.correct_german_word_input.text(), self.correct_english_word_input.text()]
        return self.correct_word_pair_list


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())
