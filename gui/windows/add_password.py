import base64
import sqlite3 as sql
from cryptography.fernet import Fernet
from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox
# import rsa
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from os import urandom
from Crypto.Cipher import AES


class AddPasswordWindow(QMainWindow):
    def __init__(self, symmetric_key):
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
        self.symmetric_key = symmetric_key

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
        securityMethod.addItem('Fernet')
        securityMethod.addItem('AES')
        # self.security = securityMethod.currentIndex()
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
                        cur.execute(("Select Password, DecodeKey from Passwords WHERE Site LIKE '%s' AND Username "
                                     "= '%s'" % (self.site, self.user)))
                        data = cur.fetchall()
                        self.symmetric_iv = cur.execute("SELECT * FROM Master").fetchone()[1]
                        if len(data) <= 0:
                            if self.security == "RSA":
                                random_generator = Random.new().read
                                RSAkey = RSA.generate(2048, random_generator)
                                # print(RSAkey)
                                self.decodeKey = RSAkey.export_key()
                                publicKey = RSAkey.publickey()
                                encryptor = PKCS1_OAEP.new(publicKey)
                                self.passwordVal = encryptor.encrypt(self.passwordVal.encode())
                                self.passwordVal = base64.b64encode(self.passwordVal)
                                self.passwordVal = self.passwordVal.decode()
                                cur.execute("INSERT INTO RSA(SITE,USERNAME) VALUES(?,?)", (self.site, self.user))
                            elif self.security == "Fernet":
                                encryptor = Fernet.generate_key()
                                self.decodeKey = encryptor
                                #self.decodeKey = encryptor
                                self.passwordVal = Fernet(encryptor).encrypt(self.passwordVal.encode())
                                self.passwordVal = base64.b64encode(self.passwordVal)
                                self.passwordVal = self.passwordVal.decode()
                                cur.execute("INSERT INTO Fernet(Site,Username) VALUES(?,?)", (self.site, self.user))
                            elif self.security == 'AES':
                                secret_key = urandom(16)
                                self.decodeKey = secret_key
                                iv = urandom(16)
                                obj = AES.new(secret_key, AES.MODE_CFB, iv)
                                self.passwordVal = obj.encrypt(self.passwordVal.encode())
                                self.passwordVal = base64.b64encode(self.passwordVal)
                                self.passwordVal = self.passwordVal.decode()
                                cur.execute("INSERT INTO AES(Site,Username,IV) VALUES(?,?,?)", (self.site, self.user,iv))


                            cur.execute("INSERT INTO Passwords(Site,Username,Password, DecodeKey) VALUES (?,?,?,?)",
                                        (self.site, self.user, self.passwordVal, self.encrypt_decode_key(self.decodeKey, self.symmetric_iv)))      
                            con.commit()
                        else:
                            print('Those credentials already exist!')
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

    def encrypt_decode_key(self, decode_key, iv):
        encryptor = AES.new(self.symmetric_key, AES.MODE_CFB, iv=iv)
        return encryptor.encrypt(decode_key)