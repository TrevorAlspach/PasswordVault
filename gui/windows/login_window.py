from os import urandom
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QMainWindow, QLabel, QPushButton
from PySide6 import QtCore
from gui.windows.main_window import MainWindow
import sqlite3 as sql
import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.MD5 as MD5

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Login here
        self.setWindowTitle("Password Vault")
        self.setFixedSize(540, 720)
        if self.is_first_login():
            self.setCentralWidget(self.setup_master())
        else:
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
            self.w = MainWindow(hash_md5(self.userInput), False)
            self.w.show()
            self.close()
        else:
            self.counter = self.counter + 1
            layout = self.centralWidget().layout()
            layout.addWidget(QLabel(str(10-self.counter) + " password attempts until data is cleared."))

    def passwordChange(self, text):
        self.userInput = text

    def is_first_login(self):
        with sql.connect("db/database.db") as con:
            cur = con.cursor()
            password = cur.execute("SELECT * FROM Master").fetchone()
        return password == None

    def setup_master(self):
        self.newMasterPassword = None
        self.confirmMasterPassword = None
        widget = QWidget()
        layout = QVBoxLayout()
        password_input = QLineEdit()
        
        label1 = QLabel("Welcome to the Password Vault App!!")
        label2 = QLabel("Please Enter your Master Password Below. Make sure its a strong password, it will be used to access all of your other passwords!")
        password_input = QLineEdit()
        password_input.textChanged.connect(self.newMasterChange)
        confirm_master = QLineEdit()
        confirm_master.textChanged.connect(self.confirmMasterChange)
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label2.setAlignment(QtCore.Qt.AlignCenter)
        confirm = QPushButton("Set Password")
        confirm.clicked.connect(self.set_password)
        label2.setWordWrap(True)
        layout.addStretch()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addStretch()
        
        layout.addWidget(QLabel("Master Password"))
        layout.addWidget(password_input)
        layout.addWidget(QLabel("Confirm Master Password"))
        layout.addWidget(confirm_master)
        layout.addWidget(confirm)
        layout.addStretch()
        layout.addStretch()

        widget.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        return widget

    def set_password(self):
        if self.newMasterPassword == self.confirmMasterPassword and self.newMasterPassword != None:
            with sql.connect("db/database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Master(password, iv) VALUES (?,?)", (SHA256.new(
                    bytes(self.newMasterPassword, encoding='utf-8')).digest(), urandom(16)))
                con.commit()
                cur.close()
            self.setCentralWidget(self.display_login())
        else:
            print("nothing to set password to")

    def newMasterChange(self, text):
        self.newMasterPassword = text

    def confirmMasterChange(self, text):
        self.confirmMasterPassword = text

def hash_md5(plaintext):
    return MD5.new(bytes(plaintext, encoding='utf-8')).digest()
