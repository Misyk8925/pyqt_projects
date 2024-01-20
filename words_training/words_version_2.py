import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *
from random import *
import sqlite3 as sq
import pandas as pd


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


        if len(self.german_list):       # if there is any word
            self.random_number = randint(0, len(self.german_list) - 1)
            self.advanced_init_ui()     # if not, display function, that should add new words
        else:
            self.display_add_new_word_function()
            if len(self.german_list):
                self.random_number = randint(0, len(self.german_list) - 1)
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
        """it takes new word from a databse column (german_word or english word) and rerurns it 

        Args:
            column (str): german_word or english_word

        Returns:
            list: list of german or english words
        """
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

        self.setStyleSheet("background-color: rgb(28, 17, 51);")

        aw_label = QLabel("Click below, if you want to add new word")
        self.layout.addWidget(aw_label)

        add_word = QPushButton("Add new word")
        add_word.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(add_word)
        add_word.clicked.connect(self.adding_new_word)
        self.btn_add_from_excel = QPushButton("Add new words from excel")
        self.btn_add_from_excel.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.btn_add_from_excel.clicked.connect(self.add_from_excel)
        self.layout.addWidget(self.btn_add_from_excel)

    def add_from_excel(self):
        try:
            # Specify the path to your Excel file
            excel_file_path = 'words_sheet.xlsx'

            df = pd.read_excel(excel_file_path, names=['german_word', 'english_word'])

            # Connect to SQLite database (adjust the database name)
            db_path = 'words_list.db'
            conn = sq.connect(db_path)
            cursor = conn.cursor()

            # Create the table if it doesn't exist

            conn = sq.connect("words_list.db")

            df.to_sql('words', conn, index=False, if_exists='append')
            # Commit the changes and close the database connection
            self.restart()

            conn.commit()
            conn.close()
        except:
            self.show_delete_msg("There is not such an excel file", "you cannot add words from it", "excel file error")      # words_sheet.xlsx

    def init_main_window_ui(self):
        self.random_number = randint(0, len(self.german_list) - 1)
        self.random_selected_word = self.german_list[self.random_number]  # random word

        self.german_word = QLabel("Word on german:", self)
        self.word = QLabel(self.random_selected_word)

        english_word_label = QLabel("Word on english: ", self)
        self.word_input = QLineEdit(self)
        self.result_label = QLabel("Result: ", self)

        self.layout.addWidget(self.german_word)
        self.layout.addWidget(self.word)
        self.layout.addWidget(english_word_label)
        self.layout.addWidget(self.word_input)
        self.layout.addWidget(self.result_label)

        btn_get_res = QPushButton("Check")
        btn_get_res.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(btn_get_res)
        btn_get_res.clicked.connect(self.get_result)

        self.btn_restart = QPushButton("Next word")
        self.btn_restart.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(self.btn_restart)
        self.btn_restart.clicked.connect(self.restart)

        self.more_options_label = QLabel("Click below, if you would like to see more options")
        self.layout.addWidget(self.more_options_label)

        self.btn_more_options = QPushButton("More options")
        self.btn_more_options.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(self.btn_more_options)
        self.btn_more_options.clicked.connect(self.more_options)

        self.words_list = QComboBox(self)
        self.words_list.setVisible(False)
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word

        self.delete_words_list = QComboBox(self)
        self.delete_words_list.setVisible(False)
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        self.setStyleSheet("background-color: rgb(28, 17, 51);")

        self.setLayout(self.layout)

    def advanced_init_ui(self):
        self.init_main_window_ui()
        self.display_add_new_word_function()

    def more_options(self):
        self.more_options_dialog = MoreOptionsDialog(self.cur, self.con, self.word, self.word_input,
                                                        self.result_label, self.random_number,self.german_word, parent=self)

        if self.more_options_dialog.exec() == QDialog.DialogCode.Accepted:
            self.words_list = self.more_options_dialog.lists_returning()[0]
            self.delete_words_list = self.more_options_dialog.lists_returning()[1]
            self.restart()
        else:
            self.restart()

    def init_output_word_list(self):
        self.edit_word_label = QLabel("If you want to EDIT any word, please select one from the list below")
        self.layout.addWidget(self.edit_word_label)

        self.words_list = QComboBox(self)
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")
        self.layout.addWidget(self.words_list)

    def init_deleting_word_list(self):
        self.delete_word_label = QLabel("If you want to DELETE any word pair, please select one from the list below")
        self.layout.addWidget(self.delete_word_label)

        self.delete_words_list = QComboBox(self)
        self.fetch_data_from_database()
        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        self.layout.addWidget(self.delete_words_list)

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


    def get_result(self):
        answer = str(self.word_input.text())
        print(answer)
        print(self.english_list[self.random_number][2:-3])

        if answer == str(self.english_list[self.random_number]):
            self.result_label.setStyleSheet("color: lightgreen;")
            self.result_label.setText("Correct")

        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Incorrect")

    def show_delete_msg(self, text, detailed_text, title):
        delete_msg = QMessageBox()
        delete_msg.setText(text)
        delete_msg.setDetailedText(detailed_text)
        delete_msg.setIcon(QMessageBox.Icon.Information)
        delete_msg.setWindowTitle(title)
        delete_msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        delete_msg.exec()


    def restart(self):
        try:
            self.german_list = DlgMain.creating_lists_of_words(self,"german_word")  # import from database word into lists
            self.english_list = DlgMain.creating_lists_of_words(self, "english_word")

            if len(self.german_list) > 1:
                bol = True
                while bol:
                    self.random_number_new = randint(0, len(self.german_list) - 1)
                    if self.random_number_new != self.random_number:
                        bol = False
                self.random_selected_word = self.german_list[self.random_number_new]  # formatted word
                self.random_number = self.random_number_new
            else:
                self.random_selected_word = self.german_list[0]

            self.german_word.setText("Word on German:")
            self.word.setText(self.random_selected_word)
            self.word_input.clear()
            self.result_label.clear()

            self.words_list.clear()
            self.fetch_data_from_database()

            for word_pair in self.word_pairs:
                self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word

            self.delete_words_list.clear()
            self.fetch_data_from_database()

            for word_pair in self.word_pairs:
                self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        except:
            self.show_delete_msg("Database has been changed! Restart the app!", "You need to restart the programme", "Changes in Database")
            self.close()

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


class MoreOptionsDialog(QDialog):
    def __init__(self, cur, con, word, word_input, result_label, random_number, german_word, parent = None):
        super().__init__()
        self.cur = cur
        self.con = con
        self.word = word
        self.word_input = word_input
        self.result_label = result_label
        self.random_number = random_number
        self.german_word = german_word
        self.init_ui()

    def init_ui(self):
        self.more_options_layout = QVBoxLayout()

        self.init_output_word_list()

        self.btn_open_editor = QPushButton("Edit this word pair")
        self.btn_open_editor.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.btn_open_editor.clicked.connect(self.show_editor_window)

        self.more_options_layout.addWidget(self.btn_open_editor)

        self.init_deleting_word_list()

        self.btn_open_delete_window = QPushButton("Delete this word pair")
        self.btn_open_delete_window.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.btn_open_delete_window.clicked.connect(self.delete_word_pair)
        self.more_options_layout.addWidget(self.btn_open_delete_window)

        self.search_word_field = QLineEdit(self)
        self.search_word_field.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.all_word_list = QListWidget(self)
        #self.all_word_list.setStyleSheet("background-color: rgb(75, 11, 144);")

        self.more_options_layout.addWidget(self.search_word_field)
        self.more_options_layout.addWidget(self.all_word_list)

        self.search_word_field.textChanged.connect(self.show_search_word_list)

        self.btn_add_from_excel = QPushButton("Add new words from excel")
        self.btn_add_from_excel.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.btn_add_from_excel.clicked.connect(self.add_from_excel)
        self.more_options_layout.addWidget(self.btn_add_from_excel)

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

        self.more_options_layout.addWidget(buttons)

        self.german_list = self.creating_lists_of_words("german_word")  # import from database word into lists
        self.english_list = self.creating_lists_of_words("english_word")

        self.setStyleSheet("background-color: rgb(28, 17, 51);")

        self.setLayout(self.more_options_layout)

    def creating_lists_of_words(self, column):      # adding new words to lists
        self.cur.execute(f"SELECT {column} FROM words")
        return [word[0] for word in self.cur.fetchall()]

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

    def init_output_word_list(self):
        self.edit_word_label = QLabel("If you want to EDIT any word, please select one from the list below")
        self.more_options_layout.addWidget(self.edit_word_label)

        self.words_list = QComboBox(self)
        self.words_list.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word
        print(type(self.words_list))
        self.more_options_layout.addWidget(self.words_list)

    def init_deleting_word_list(self):
        self.delete_word_label = QLabel("If you want to DELETE any word pair, please select one from the list below")
        self.more_options_layout.addWidget(self.delete_word_label)

        self.delete_words_list = QComboBox(self)
        self.delete_words_list.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.fetch_data_from_database()
        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        self.more_options_layout.addWidget(self.delete_words_list)

    def show_editor_window(self):
        # Создаем и отображаем диалоговое окно при выборе элемента из выпадающего списка
        self.selected_item = self.words_list.currentText()

        self.corrections_dialog = EditorDialog(str(self.selected_item), self.cur, self.con, parent=self)

        # Use the result of the first exec() call
        if self.corrections_dialog.exec() == QDialog.DialogCode.Accepted:

            self.updating_corrections()
            # Update the UI or perform other actions as needed
        else:
            print("Operation has been cancelled")

        DlgMain.restart(self)

    def updating_corrections(self):
        user_corrections_input = self.corrections_dialog.get_corrections_user_input()

        old_word = str(self.selected_item).split('   ')
        """print(old_word)
        print((user_corrections_input[0], old_word[0]))
        print((user_corrections_input[1], old_word[2]))"""
        self.cur.execute("UPDATE words SET german_word = ? WHERE german_word = ?",
                         (user_corrections_input[0], old_word[0]))

        self.cur.execute("UPDATE words SET english_word = ? WHERE english_word = ?",
                         (user_corrections_input[1], old_word[2]))
        self.con.commit()

    def delete_word_pair(self):
        try:
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
                DlgMain.restart(self)
            else:
                QMessageBox.critical(self, "Canceled", "User clicked CANCEL")
        except:
            DlgMain.show_delete_msg(self, "Database has been changed! Restart the app!", "You need to restart the programme", "Changes in Database")
            self.close()

    def show_search_word_list(self, text):
        matching_words_german = [word for word in self.german_list if text.lower() in word.lower()]
        matching_words_english = [word for word in self.english_list if text.lower() in word.lower()]

        self.all_word_list.clear()

        for word in matching_words_german:
            item = QListWidgetItem(word)
            item.setForeground(QColor("Light blue"))
            self.all_word_list.addItem(item)

        for word in matching_words_english:
            item = QListWidgetItem(word)
            item.setForeground(QColor("Light yellow"))
            self.all_word_list.addItem(item)

    def add_from_excel(self):

        # Specify the path to your Excel file
        excel_file_path = 'words_sheet.xlsx'

        df = pd.read_excel(excel_file_path, names=['german_word', 'english_word'])

        # Connect to SQLite database (adjust the database name)
        db_path = 'words_list.db'
        conn = sq.connect(db_path)
        cursor = conn.cursor()

        # Create the table if it doesn't exist

        conn = sq.connect("words_list.db")

        df.to_sql('words', conn, index=False, if_exists='append')
        # Commit the changes and close the database connection
        DlgMain.restart(self)
        conn.commit()
        conn.close()

    def lists_returning(self):
        return [self.words_list, self.delete_words_list]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel, QLineEdit, QPushButton, QListWidget, QComboBox {color: white; }")
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())
