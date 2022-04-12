from tabnanny import check
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PySide6 import QtCore
import sqlite3 as sql
from PySide6.QtCore import Slot
import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.SHA3_256 as SHA256_3
from password_cracking.john import run_john_wordlist

class ChangeMaster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.currentMaster = ""
        self.newMasterPassword = ""
        self.confirmMasterPassword = ""
        self.setWindowTitle("Change Master Password")
        self.setFixedSize(540, 720)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.showMasterPassChangeWindow())

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
                con.commit()
                cur.close()
                self.close()

    def checkPasswordStrength(self):
        password_found = run_john_wordlist(SHA256.new(bytes(self.newMasterPassword, encoding='utf-8')).hexdigest())
        msg = QMessageBox()
        msg.setFixedSize(600, 600)
        if password_found == True:
            msg.setText("Your password is weak. It's used very commonly and easily be cracked ")
        elif password_found == False:
            msg.setText("Your password is strong.It is not used very commonly")
        else:
            return
        msg.setWindowTitle("Password Info")
        msg.exec_()
        # Don't know how to get this to print yet
        # layout = self.()
        # if not masterMatches:
        #     layout.addWidget(QLabel("Master Password you entered does not match the previous master password."))
        # elif not newMasterMatches:
        #     layout.addWidget(QLabel("New passwords do not match."))

