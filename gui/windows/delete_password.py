import base64
import sqlite3 as sql
from cryptography.fernet import Fernet
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox
#import rsa
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP




class DeletePasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.site = ""
        self.user = ""
        self.passwordVal = ""
        self.setWindowTitle("Delete Password")
        self.setFixedSize(540, 355)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.showDeletePassWindow())


    def showDeletePassWindow(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Which password would you like to delete?"))
        options = QComboBox()
        with sql.connect("db/database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT Site FROM Passwords")
            sites = cur.fetchall()
            for site in sites:
                thesite = str(site)
                thesite = thesite.strip("(),'")
                options.addItem(thesite)
            cur.close()
        options.currentTextChanged.connect(self.siteChange)
        layout.addWidget(options)
        delete = QPushButton("Delete Selected Password")
        delete.clicked.connect(self.deleteClicked)
        layout.addWidget(delete)
        widget.setLayout(layout)

        return widget

        
    def deleteClicked(self):
        con = sql.connect("db/database.db")
        cur = con.cursor()
        cur.execute("delete from Passwords where Site=?",(self.site,))
        con.commit()
        cur.close()
        self.close()
         
    def siteChange(self, text):
        self.site = text