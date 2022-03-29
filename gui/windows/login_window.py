from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QMainWindow, QLabel
from PySide6 import QtCore


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Login here
        self.setWindowTitle("Password Vault")
        self.setFixedSize(540, 720)
        self.setCentralWidget(self.display_login())

    def display_login(self):
        widget = QWidget()
        layout = QVBoxLayout()
        password_input = QLineEdit()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(QLabel("Enter Master Password"))
        layout.addWidget(password_input)
        widget.setLayout(layout)

        return widget
