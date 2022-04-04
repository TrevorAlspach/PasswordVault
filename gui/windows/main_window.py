from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide6 import QtCore
import sqlite3 as sql
from gui.windows.add_password import AddPasswordWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Vault")
        self.setFixedSize(540, 720)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.showMainWindow())
        self.w = None

    def showMainWindow(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        addPasswordButton = QPushButton("Add Password")
        addPasswordButton.clicked.connect(self.addPassword)
        layout.addWidget(addPasswordButton)
        refreshButton = QPushButton("Refresh")
        refreshButton.clicked.connect(self.refresh)
        layout.addWidget(refreshButton)

        widget.setLayout(layout)
        with sql.connect('db/database.db') as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Passwords")
            print(cur.fetchall())

        return widget

    def addPassword(self):
        self.w = AddPasswordWindow()
        self.w.show()

    def refresh(self):
        self.w = MainWindow()
        self.w.show()
        self.close()


