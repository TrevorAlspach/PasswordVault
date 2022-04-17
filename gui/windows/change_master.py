from os import urandom
from tabnanny import check
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PySide6 import QtCore
import sqlite3 as sql
from PySide6.QtCore import Slot
import Crypto.Hash.SHA256 as SHA256
from password_cracking.john import run_john_wordlist
import Crypto.Hash.MD5 as MD5
import Crypto.Cipher.AES as AES

class ChangeMaster(QMainWindow):
    def __init__(self, symmetric_key):
        super().__init__()
        self.currentMaster = ""
        self.newMasterPassword = ""
        self.confirmMasterPassword = ""
        self.setWindowTitle("Change Master Password")
        self.setFixedSize(540, 720)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.showMasterPassChangeWindow())
        self.symmetric_key = symmetric_key

    def showMasterPassChangeWindow(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Current Master Password"))
        curMaster = QLineEdit()
        curMaster.textChanged.connect(self.curMasterChange)
        layout.addWidget(curMaster)
        layout.addWidget(QLabel("New Master Password"))
        newMaster = QLineEdit()
        newMaster.textChanged.connect(self.newMasterChange)
        layout.addWidget(newMaster)
        layout.addWidget(QLabel("Confirm New Master Password"))
        confirmMaster = QLineEdit()
        confirmMaster.textChanged.connect(self.confirmMasterChange)
        layout.addWidget(confirmMaster)
        confirm = QPushButton("Confirm")
        confirm.clicked.connect(self.updateTable)
        layout.addWidget(confirm)
        checkStrength = QPushButton("Check Password Strength")
        checkStrength.clicked.connect(self.checkPasswordStrength)
        layout.addWidget(checkStrength)
        widget.setLayout(layout)

        return widget

    def curMasterChange(self, text):
        self.currentMaster = text

    def newMasterChange(self, text):
        self.newMasterPassword = text

    def confirmMasterChange(self, text):
        self.confirmMasterPassword = text

    def updateTable(self):
        masterMatches = False
        newMasterMatches = False
        with sql.connect("db/database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Master")
            oldMaster = cur.fetchone()
            oldMaster = oldMaster[0]
            print(oldMaster)
            cur.close()
        if SHA256.new(bytes(self.currentMaster, encoding='utf-8')).digest() != oldMaster:
            print("The Master password you entered does not match")
        else:
            masterMatches = True
        if self.newMasterPassword == self.confirmMasterPassword and not self.newMasterPassword.isspace():
            print("The new master password is ", self.newMasterPassword)
            newMasterMatches = True

        if masterMatches and newMasterMatches:
            with sql.connect("db/database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Master SET password = ?", (SHA256.new(
                    bytes(self.newMasterPassword, encoding='utf-8')).digest(),))
                #self.reencrypt_with_new_master(self.newMasterPassword, con)
                cur.execute("DELETE FROM Passwords")
                con.commit()
                cur.close()
            
            self.close()

    def checkPasswordStrength(self):
        symbols = "!@# $%^&*()-+?_=,<>/"
        msg = QMessageBox()
        msg.setFixedSize(600, 600)
        if len(self.newMasterPassword) <= 8:
            #not long enough
            msg.setText(
                "Your password is weak due to its short length. It could be brute forced easily")
            msg.setWindowTitle("Password Info")
            msg.exec_()
            return

        if (self.newMasterPassword.isdecimal()):
            #Only digits
             msg.setText(
                "Your password is weak since it is only digits.\n Try adding some alphabetic characters/symbols")
             msg.setWindowTitle("Password Info")
             msg.exec_()
             return
        
        if (not any(c in symbols for c in self.newMasterPassword)):
            msg.setText(
                "Your password is weak since it has no symbols.\n Try adding any of !@# $%^&*()-+?_=,<>/")
            msg.setWindowTitle("Password Info")
            msg.exec_()
            return
        
        password_found = run_john_wordlist(SHA256.new(bytes(self.newMasterPassword, encoding='utf-8')).hexdigest())
        
        if password_found == True:
            msg.setText(
                "While the length is good, your password is weak since \nit's used very commonly and is easily cracked via a wordlist")
        elif password_found == False:
            msg.setText("Adequate password length and composition.\n It is not used very commonly.\n Strong Password")
        else:
            return
        msg.setWindowTitle("Password Info")
        msg.exec_()
