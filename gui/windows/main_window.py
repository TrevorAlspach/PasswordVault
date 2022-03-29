from PySide6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Vault")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
