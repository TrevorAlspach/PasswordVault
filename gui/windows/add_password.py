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
        self.security = "RSA"
        self.decodeKey = ""

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
        layout.addWidget((QLabel("Encryption/Decryption Method")))
        securityMethod = QComboBox()
        securityMethod.addItem('RSA')
        securityMethod.addItem('Other')
        #self.security = securityMethod.currentIndex()
        securityMethod.currentTextChanged.connect(self.securityChange)
        layout.addWidget(securityMethod)
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
                        if self.security == "RSA":
                            random_generator = Random.new().read
                            RSAkey = RSA.generate(2048,random_generator)
                            #print(RSAkey)
                            self.decodeKey = RSAkey.export_key()

                            publicKey = RSAkey.publickey()
                            encryptor = PKCS1_OAEP.new(publicKey)
                            self.passwordVal = encryptor.encrypt(self.passwordVal.encode())
                            print(self.passwordVal)
                            self.passwordVal = base64.b64encode(self.passwordVal)
                            self.passwordVal = self.passwordVal.decode()
                            #print(self.passwordVal)

                        cur.execute("INSERT INTO Passwords(Site,Username,Password, DecodeKey) VALUES (?,?,?,?)",
                                    (self.site, self.user, self.passwordVal,self.decodeKey))
                        con.commit()
                        cur.close()
                    self.close()

    def siteNameChange(self, text):
        self.site = text

    def usernameChange(self, text):
        self.user = text

    def passwordChange(self, text):
        self.passwordVal = text

    def securityChange(self, text):
        self.security = text