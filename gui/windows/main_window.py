from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
import sqlite3 as sql
from gui.windows.add_password import AddPasswordWindow


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        Qt.AlignCenter
        self.horizontalHeaders = [''] * 3
        self.setHeaderData(0, Qt.Horizontal, "Site")
        self.setHeaderData(1, Qt.Horizontal, "Username")
        self.setHeaderData(2, Qt.Horizontal, "Password")
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[section]
            except:
                pass
        return super().headerData(section, orientation, role)


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

        # widget.setLayout(layout)
        with sql.connect('db/database.db') as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Passwords")
            data = cur.fetchall()
            print(data)
        table = QtWidgets.QTableView()
        model = TableModel(data)
        table.setModel(model)
        layout.addWidget(table)
        widget.setLayout(layout)
        return widget

    def addPassword(self):
        self.w = AddPasswordWindow()
        self.w.show()

    def refresh(self):
        self.w = MainWindow()
        self.w.show()
        self.close()
