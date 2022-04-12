from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QMainWindow, QLabel, QPushButton
from PySide6 import QtCore
from gui.windows.main_window import MainWindow
import sqlite3 as sql
import Crypto.Hash.SHA3_256 as SHA256

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Login here
        self.setWindowTitle("Password Vault")
        self.setFixedSize(540, 720)
        self.setCentralWidget(self.display_login())
        self.userInput = ""
        self.w = None
        self.counter = 0

    def display_login(self):
        widget = QWidget()
        layout = QVBoxLayout()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)  # Hides password input
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Enter Master Password"))
        layout.addWidget(password_input)
        password_input.textChanged.connect(self.passwordChange)
        loginButton = QPushButton("Submit")
        loginButton.clicked.connect(self.checkCredentials)
        layout.addWidget(loginButton)
        widget.setLayout(layout)

        return widget

    def checkCredentials(self):
        with sql.connect("db/database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Master")
            temp = cur.fetchall()
            cur.close()
        temp = temp[0]
        if SHA256.new(bytes(self.userInput, encoding='utf-8')).digest() == temp[0]:
            self.w = MainWindow(False)
            self.w.show()
            self.close()
        else:
            self.counter = self.counter + 1
            layout = self.centralWidget().layout()
            layout.addWidget(QLabel(str(10-self.counter) + " password attempts until data is cleared."))

    def passwordChange(self, text):
        self.userInput = text


#Crypto.Hash.SHA3_256.new(bytes(self.userInput, encoding='utf-8')).digest()
