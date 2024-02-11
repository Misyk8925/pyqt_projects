import sys
from PyQt6.QtWidgets import *
import sqlite3 as sq
import pandas as pd


class DatabaseManager:
    db_list = []

    def __init__(self, db_name):
        self.db_path = f"{db_name}.db"
        self.con = sq.connect(self.db_path)
        self.cur = self.con.cursor()
        self.create_table()
        DatabaseManager.db_list.append(self.db_path)  # Add new database to the list

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS words 
            (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                german_word TEXT,
                english_word TEXT,
                counter INTEGER DEFAULT 0
            )
        """)
        self.con.commit()

    def fetch_words(self, column):
        self.cur.execute(f"SELECT {column} FROM words ORDER BY counter")
        return [word[0] for word in self.cur.fetchall()]

    def add_word(self, german, english):
        self.cur.execute("INSERT INTO words (german_word, english_word) VALUES (?, ?)", (german, english))
        self.con.commit()

    def add_words_from_excel(self, excel_path='words_sheet.xlsx'):
        try:
            df = pd.read_excel(excel_path, names=['german_word', 'english_word'])
            df.to_sql('words', self.con, index=False, if_exists='append')
            self.con.commit()
        except Exception as e:
            print(f"Error adding words from Excel: {e}")


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


class DlgMain(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.german_list = self.db_manager.fetch_words("german_word")
        self.english_list = self.db_manager.fetch_words("english_word")
        if self.german_list:
            self.init_main_window_ui()
        else:
            self.display_add_new_word_function()

    def display_add_new_word_function(self):
        aw_label = QLabel("Click below if you want to add a new word")
        self.layout.addWidget(aw_label)

        add_word_button = UIComponents.create_button("Add new word", self.adding_new_word)
        self.layout.addWidget(add_word_button)

        add_from_excel_button = UIComponents.create_button("Add new words from excel", self.add_from_excel)
        self.layout.addWidget(add_from_excel_button)

        UIComponents.apply_stylesheet(self)



    def add_from_excel(self):
        self.db_manager.add_words_from_excel()
        self.restart()

    def init_main_window_ui(self):
        self.setStyleSheet("background-color: rgb(81, 0, 135, 255);")
        # ... rest of the code for main window UI

    def restart(self):
        self.german_list = self.db_manager.fetch_words("german_word")
        self.english_list = self.db_manager.fetch_words("english_word")
        # ... rest of the code for restarting


# Other classes and functions can be similarly refactored.

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a DatabaseManager instance with a specific database name
    db_manager = DatabaseManager("your_database_name")

    app.setStyleSheet("QLabel, QLineEdit, QPushButton, QListWidget, QComboBox {color: white;}")
    dlgMain = DlgMain(db_manager)
    dlgMain.show()
    sys.exit(app.exec())
