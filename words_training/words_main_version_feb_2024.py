import logging
import sys
from sqlalchemy import *
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *
import sqlite3 as sq
import pandas as pd
from PyQt6.QtCore import QTimer


class MyDatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_path = f"{db_name}.db"
        self.con = sq.connect(self.db_path)
        self.cur = self.con.cursor()
        self.table_name = "words"
        self.create_table()

    def create_table(self):
        try:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS {} 
                (
                    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    german_word TEXT,
                    english_word TEXT,
                    counter INTEGER DEFAULT 0
                )
            """.format(self.table_name))
            self.con.commit()
        except sq.Error as e:
            logging.error(f"Error creating words: {e}")

    def fetch_words(self, column):
        try:
            self.cur.execute(f"SELECT {column} FROM words ORDER BY counter")
            return [word[0] for word in self.cur.fetchall()]
        except sq.Error as e:
            logging.error(f"Error fetching words: {e}")
            return []

    def return_db_path(self):
        return self.db_name

    def return_table_name(self):
        return self.table_name, self.cur, self.con

    def add_words_from_excel(self, excel_path='words_sheet.xlsx'):
        try:
            df = pd.read_excel(excel_path, names=['german_word', 'english_word'])
            df.to_sql('words', self.con, index=False, if_exists='append')
            self.con.commit()
        except Exception as e:
            print(f"Error adding words from Excel: {e}")

    def delete_word(self, german_word, english_word):
        try:
            self.cur.execute("DELETE FROM words WHERE german_word = ? AND english_word = ?",
                             (german_word, english_word))
            self.con.commit()
        except sq.Error as e:
            logging.error(f"Error deleting word from 'words' table: {e}")

    def update_corrections(self, user_corrections_input, old_word):
        try:
            self.cur.execute("UPDATE words SET german_word = ? WHERE german_word = ?",
                             (user_corrections_input[0], old_word[0]))

            self.cur.execute("UPDATE words SET english_word = ? WHERE english_word = ?",
                             (user_corrections_input[1], old_word[2]))
            self.con.commit()
        except sq.Error as e:
            logging.error(f"Error updating corrections in 'words' table: {e}")

class UIComponents:
    @staticmethod
    def apply_stylesheet(widget):
        widget.setStyleSheet("background-color: rgb(28, 17, 51); color: white;")

    @staticmethod
    def create_button(text, click_handler):
        button = QPushButton(text)
        button.setStyleSheet("background-color: rgb(75, 11, 144);")
        button.clicked.connect(click_handler)
        return button


class DlgStart(QDialog):
    def __init__(self):
        super().__init__()

        self.current_db_index = 0

        self.db_list = self.load_db_list()  # Initialize db_list here
        try:
            self.db_manager = MyDatabaseManager(self.db_list[self.current_db_index])
        except IndexError:
            self.load_db_list()

        self.layout = QVBoxLayout(self)
        self.display_add_new_database_function()

    def display_add_new_database_function(self):
        db_label = QLabel("Select a database or create a new one:")
        self.layout.addWidget(db_label)

        self.db_combobox = QComboBox()
        self.db_combobox.addItems(self.db_list)
        self.db_combobox.currentIndexChanged.connect(self.switch_database)
        self.layout.addWidget(self.db_combobox)

        new_db_button = UIComponents.create_button("Create New Database", self.create_new_database)
        self.layout.addWidget(new_db_button)

        start_working_button = UIComponents.create_button("Start Working", self.start_working)
        self.layout.addWidget(start_working_button)

        UIComponents.apply_stylesheet(self)

    def switch_database(self, index):
        self.current_db_index = index
        self.db_manager = self.create_db_manager()
        return self.db_manager

    def create_new_database(self):
        new_db_name, ok = QInputDialog.getText(self, "New Database", "Enter the name for the new database:")
        if ok and new_db_name:
            self.db_list.append(new_db_name)
            self.db_combobox.addItem(new_db_name)
            self.db_combobox.setCurrentIndex(len(self.db_list) - 1)
            self.switch_database(len(self.db_list) - 1)
            self.save_db_list()  # Save the updated database list

    def start_working(self):
        db = self.switch_database(self.current_db_index)
        dlm = DlgMain(db, self.current_db_name, self.db_list, self.current_db_index, self.db_manager, parent=self)
        e = dlm.exec()
        if e == QDialog.DialogCode.Accepted:
            print("Dialog accepted")

    def create_db_manager(self):
        self.current_db_name = self.db_list[self.current_db_index]
        return MyDatabaseManager(self.current_db_name)

    def return_db_path(self):
        return self.current_db_name

    def load_db_list(self):
        try:
            file = open("db_list.txt", "r")
            if len(file.read()) == 0:
                with open("db_list.txt", "w") as file:
                    file.write("word_list")
            with open("db_list.txt", "r") as file:
                return file.read().splitlines()
            with open("db_list.txt", "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def save_db_list(self):
        with open("db_list.txt", "w") as file:
            file.write("\n".join(self.db_list))

class DlgMain(QDialog):
    def __init__(self, database, current_db_name, db_list, current_db_index, db_manager, parent=None):
        super().__init__()
        self.setWindowTitle("Words training")
        self.current_db_name = current_db_name
        self.layout = QVBoxLayout(self)  # add vertical layout
        self.german_word = QLabel(" ", self)
        self.db_list = db_list
        self.current_db_index = current_db_index
        self.db_manager = db_manager

        #self.database = database  # Create database with words
        self.index = 0
        self.counter = 0

        self.word_pairs = []

        self.german_word = QLabel("Word on german:", self)
        # self.db_manager = DlgStart.create_db_manager(self)

        self.german_list = self.db_manager.fetch_words("german_word")
        self.english_list = self.db_manager.fetch_words("english_word")
        self.table_name, self.cur, self.con = self.db_manager.return_table_name()

        self.word_input = QLineEdit(self)
        self.result_label = QLabel("Result: ", self)
        self.word = QLabel()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handle_timeout)

        if self.german_list:  # if there is any word
            self.selected_word = self.german_list[self.index]  # first word
            self.word = QLabel(self.selected_word)
            self.advanced_init_ui()  # if not, display function, that should add new words
        else:

            self.display_add_new_word_function()

            if self.german_list:
                self.selected_word = self.german_list[self.index]  # first word
                self.word = QLabel(self.selected_word)

                self.init_main_window_ui()  # start main window

    def creating_lists_of_words(self, column):  # adding new words to lists
        """it takes new word from a databse column (german_word or english word) and rerurns it 

        Args:
            column (str): german_word or english_word

        Returns:
            list: list of german or english words
        """

        self.cur.execute(f"SELECT {column} FROM words ORDER BY counter")
        return [word[0] for word in self.cur.fetchall()]

    def fetch_data_from_database(self):
        try:
            with sq.connect(f"{self.current_db_name}.db") as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT german_word FROM words")
                german_data = cursor.fetchall()

                cursor.execute("SELECT english_word FROM words")
                english_data = cursor.fetchall()

                # Using zip to combine corresponding elements from german_data and english_data
                self.word_pairs = list(zip(german_data, english_data))


        except sq.Error as e:
            print(f"Database error: {e}")

    def adding_new_word(self):
        dialog = InputDialog()  # add new window, where user can add new word
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:  # if dialog window has finished
            user_input = dialog.get_user_input()

            self.cur.execute("INSERT INTO words (german_word, english_word) VALUES (?, ?)", user_input)
            self.con.commit()  # update the database
            add_german = str(user_input[0])
            add_german += " "
            self.german_list.append(add_german)

            add_english = str(user_input[1])
            add_english += " "

            self.english_list.append(add_english)

            if len(self.german_list) == 1:
                self.advanced_init_ui()  # if there is only one word, start main window

            elif len(self.german_list) > 1:
                self.restart()
        else:
            print("Operation has been cancelled")

    def display_add_new_word_function(self):

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
        self.db_manager.add_words_from_excel()
        self.restart()

    def init_main_window_ui(self):
        self.selected_word = self.german_list[self.index]  # first word

        self.german_word = QLabel("Word on german:", self)
        self.word = QLabel(self.selected_word)

        english_word_label = QLabel("Word on english: ", self)
        self.word_input = QLineEdit(self)
        self.result_label = QLabel("Result: ", self)

        self.layout.addWidget(self.german_word)
        self.layout.addWidget(self.word)
        self.layout.addWidget(english_word_label)
        self.layout.addWidget(self.word_input)
        self.layout.addWidget(self.result_label)

        self.btn_get_res = QPushButton("Check")
        self.btn_get_res.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(self.btn_get_res)
        self.btn_get_res.clicked.connect(self.get_result)

        self.btn_show_correct_answer = QPushButton("Show correct answer")
        self.btn_show_correct_answer.setStyleSheet("background-color: rgb(75, 11, 144);")
        self.layout.addWidget(self.btn_show_correct_answer)
        self.btn_show_correct_answer.clicked.connect(self.show_correct_answer)

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
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word
        self.words_list.setVisible(False)

        self.delete_words_list = QComboBox(self)
        self.delete_words_list.setVisible(False)
        self.fetch_data_from_database()

        for word_pair in self.word_pairs:
            self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")

        self.setStyleSheet("background-color: rgb(81, 0, 135, 255);")

        self.setLayout(self.layout)

    def show_correct_answer(self):
        w = str(self.english_list[self.index])
        self.show_msg(w, "It was a correct word form", "Correct word")
        self.restart()

    def advanced_init_ui(self):

        if not self.german_list or not self.english_list:
            # Display a message or handle the situation where the lists are empty
            self.show_msg("kolobok", "It was a correct word form", "Correct word")

        self.init_main_window_ui()
        self.display_add_new_word_function()

    def more_options(self):
        self.more_options_dialog = MoreOptionsDialog(self.cur, self.con, self.word, self.word_input,
                                                     self.result_label, self.german_word, self.index,
                                                     self.btn_get_res, self.db_list, self.current_db_name,
                                                     self.current_db_index, self.table_name, self.german_list,
                                                     self.english_list, parent=self)

        if self.more_options_dialog.exec() == QDialog.DialogCode.Accepted:
            self.words_list = self.more_options_dialog.lists_returning()[0]
            self.delete_words_list = self.more_options_dialog.lists_returning()[1]
            self.restart()
        else:
            self.restart()



    def get_result(self):

        answer = str(self.word_input.text())

        res = str(self.english_list[self.index])

        if answer == res:
            self.result_label.setStyleSheet("color: lightgreen;")
            self.result_label.setText("Correct")
            self.counter += 5
            self.cur.execute("UPDATE words SET counter = counter + ? WHERE english_word = ?",
                             (self.counter, answer))
            self.counter = 0
            self.con.commit()

            # Start the timer with a 1-second timeout
            self.timer.start(1000)

        else:
            self.result_label.setStyleSheet("color: red;")
            self.result_label.setText("Incorrect")
            self.counter += 1
            self.cur.execute("UPDATE words SET counter = counter + ? WHERE english_word = ?",
                             (self.counter, res))

            self.counter = 0
            self.con.commit()

    def show_msg(self, text, detailed_text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setDetailedText(detailed_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        msg.setStyleSheet("""
            QMessageBox {
                color: white;
            }
            QTextEdit {
                background-color: blue;  /* Change the background color of the detailed text area */
                color: white;  /* Change the text color of the detailed text area */
            }
            QPushButton {
                background-color: blue;  /* Change the background color of buttons */
                color: white;  /* Change the text color of buttons */
            }
        """)
        msg.exec()

    def restart(self):

         try:
            self.german_list = self.db_manager.fetch_words("german_word")  # import from database word into lists
            self.english_list = self.db_manager.fetch_words("english_word")
            self.index = 0
            self.selected_word = self.german_list[self.index]

            self.german_word.setText("Word on German:")
            self.word.setText(self.selected_word)
            self.word_input.clear()
            self.result_label.clear()

            self.words_list = QComboBox(self)
            self.fetch_data_from_database()

            for word_pair in self.word_pairs:
                self.words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word

            self.delete_words_list = QComboBox(self)
            self.fetch_data_from_database()

            for word_pair in self.word_pairs:
                self.delete_words_list.addItem(f"{str(word_pair[0])[2:-3]}   -   {str(word_pair[1])[2:-3]}")  # formatted word
         except:
            self.show_msg("Database has been changed! Restart the app!", "You need to restart the programme", "Changes in Database")
            self.close()

    def handle_timeout(self):
        # Code to execute after the timeout (1 second)
        self.restart()



class InputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        warning = QLabel("Be careful not to make a mistake!", self)
        layout.addWidget(warning)
        self.setstylesheet("background-color: rgb(81, 0, 135, 255);")

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
    def __init__(self, cur, con, word, word_input, result_label, german_word, btn_get_res, index, db_list, current_db_name, current_db_index, table_name, german_list, english_list, parent=None):
        super().__init__(parent=parent)
        self.current_db_name = current_db_name
        self.cur = cur
        self.con = con
        self.word = word
        self.word_input = word_input
        self.result_label = result_label
        self.german_word = german_word
        self.index = index
        self.german_list = german_list
        self.english_list = english_list
        self.btn_get_res = btn_get_res
        self.db_list = db_list
        self.current_db_index = current_db_index
        self.db_manager = DlgStart.create_db_manager(self)
        self.table_name = table_name
        self.word_pairs = []

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
        # self.all_word_list.setStyleSheet("background-color: rgb(75, 11, 144);")

        self.more_options_layout.addWidget(self.search_word_field)
        self.more_options_layout.addWidget(self.all_word_list)

        self.search_word_field.textChanged.connect(self.show_search_word_list)

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

        self.setStyleSheet("background-color: rgb(28, 17, 51);")

        self.setLayout(self.more_options_layout)

    def creating_lists_of_words(self, column):  # adding new words to lists
        self.cur.execute(f"SELECT {column} FROM words")
        return [word[0] for word in self.cur.fetchall()]

    def fetch_data_from_database(self):
        try:
            with sq.connect(f"{self.current_db_name}.db") as connection:
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

            DlgMain.show_msg(self, "Lists have been changed! Restart this window to them!",
                             "If you want to see new lists of words, please restart this window.",
                             "Lists have been changed")
        else:
            print("Operation has been cancelled")

        DlgMain.restart(self)

    def updating_corrections(self):
        user_corrections_input = self.corrections_dialog.get_corrections_user_input()

        old_word = str(self.selected_item).split('   ')
        self.db_manager.update_corrections(user_corrections_input, old_word)

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

                self.db_manager.delete_word(selected_word_pair[0], selected_word_pair[2])

                self.con.commit()
                QMessageBox.information(self, "Title", "You have just deleted the selected word pair")
                DlgMain.restart(self)
                DlgMain.show_msg(self, "Lists have been changed! Restart this window to see them!", "If you want to see new lists of words, please restart this window.", "Lists have been changed")
                # self.more_options_layout.addWidget(self.delete_words_list)

            else:
                QMessageBox.critical(self, "Canceled", "User clicked CANCEL")
        except:
            DlgMain.show_msg(self, "Database has been changed! Restart the app!", "You need to restart the programme",
                             "Changes in Database")
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

    def lists_returning(self):
        return [self.words_list, self.delete_words_list]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
                        QLabel, QLineEdit, QPushButton, QListWidget, QComboBox {color: white; }
                        QMessageBox { background-color: blue; color: white; }
    """)
    dlgMain = DlgStart()
    dlgMain.show()
    sys.exit(app.exec())
