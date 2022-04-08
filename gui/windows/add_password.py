from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PySide6 import QtCore
import sqlite3 as sql
from PySide6.QtCore import Slot


class AddPasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.site = ""
        self.user = ""
        self.passwordVal = ""
        self.setWindowTitle("Add Password")
        self.setFixedSize(540, 720)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.showAddPassWindow())

    def showAddPassWindow(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Site Name"))
        siteName = QLineEdit()
        siteName.textChanged.connect(self.siteNameChange)
        layout.addWidget(siteName)
        layout.addWidget(QLabel("Username"))
        username = QLineEdit()
        username.textChanged.connect(self.usernameChange)
        layout.addWidget(username)
        layout.addWidget(QLabel("Password"))
        password = QLineEdit()
        password.textChanged.connect(self.passwordChange)
        layout.addWidget(password)
        add = QPushButton("Add")
        add.clicked.connect(self.addToTable)
        layout.addWidget(add)
        widget.setLayout(layout)

        return widget

    @Slot()
    def addToTable(self):
        if not self.site.isspace() and self.site != "":
            if not self.user.isspace() and self.user != "":
                if not self.passwordVal.isspace() and self.passwordVal != "":
                    with sql.connect("db/database.db") as con:
                        cur = con.cursor()
                        cur.execute("INSERT INTO Passwords(Site,Username,Password) VALUES (?,?,?)",
                                    (self.site, self.user, self.passwordVal))
                        con.commit()
                        cur.close()
                    self.close()

    def siteNameChange(self, text):
        self.site = text

    def usernameChange(self, text):
        self.user = text

    def passwordChange(self, text):
        self.passwordVal = text
