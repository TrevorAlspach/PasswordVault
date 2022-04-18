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
            cur.execute("SELECT Username FROM Passwords")
            names = cur.fetchall()
            options.addItem("Please select a site and username")
            for x in range(len(sites)):
                thesite = str(sites[x])
                theuser = str(names[x])
                thesite = thesite.strip("(),'")
                theuser = theuser.strip("(),'")
                options.addItem(thesite + " - " + theuser)
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
        cur.execute("delete from Passwords where Site=? AND Username=?",(self.site,self.name,))
        con.commit()
        cur.close()
        self.close()
         
    def siteChange(self, text):
        thesite = ""
        theuser = ""
        first = 0
        for x in range(len(text)):
            if(first == 1):
                theuser = theuser + text[x]
            if(first == 0):
                thesite = thesite + text[x]
                if(text[x] == " "):
                    first = 1
        theuser = theuser.lstrip("-")
        theuser = theuser.strip()
        thesite = thesite.strip()
        print(thesite)
        print(theuser)
        self.site = thesite
        self.name = theuser
        
        