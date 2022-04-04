from PySide6 import QtWidgets
import db.functions as db
import os
import sys
import db.database
from gui.windows.main_window import MainWindow
from gui.windows.login_window import LoginWindow

if __name__ == "__main__":
    # run the app
    app = QtWidgets.QApplication(sys.argv)
    #db.create_tables()

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())
