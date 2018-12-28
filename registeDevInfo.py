from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QGridLayout, QComboBox

from PyQt5.QtCore import QVariant

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator

import controlDatabase


class RegisteDeviceDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Regular expression
        idRange = "(^[0-9]*$)"  # 숫자만
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression

        idRegular = QRegExp(idRange)
        ipRegular = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")

        idValidator = QRegExpValidator(idRegular, self)
        ipValidator = QRegExpValidator(ipRegular, self)

        self.IdentEdit = QLineEdit()
        self.IdentEdit.setValidator(idValidator)
        self.NameEdit = QLineEdit()
        self.CodeEdit = QLineEdit()
        self.IPAddEdit = QLineEdit()
        self.IPAddEdit.setValidator(ipValidator)
        self.RegionEdit_1 = QLineEdit()
        self.RegionEdit_2 = QLineEdit()
        self.TypeComboEdit = QComboBox()

        self.InitUI()
        print("dialog 초기화")
        self.SetInitText()

    def keyPressEvent(self, event):
        if ((not event.modifiers() and
             event.key() == Qt.Key_Return) or
                (event.modifiers() == Qt.KeypadModifier and
                 event.key() == Qt.Key_Enter)):
            event.accept()
        else:
            super(QDialog, self).keyPressEvent(event)

    def InitUI(self):

        identLabel = QLabel('장비ID')
        nameLabel = QLabel('장비이름')
        codeLabel = QLabel('장비별칭')
        ipAddLabel = QLabel('장비IP')
        regionLabel_1 = QLabel('설치장소(모국)')
        regionLabel_2 = QLabel('설치장소(자국)')
        typeLabel = QLabel('장비타입')

        regButton = QPushButton()
        regButton.setText('등록')
        regButton.clicked.connect(self.SaveDeviceInfo)

        self.viewButton = QPushButton()
        self.viewButton.setText('장비보기')

        exitButton = QPushButton()
        exitButton.setText('나가기')
        exitButton.pressed.connect(self.close)

        hBox = QHBoxLayout()
        vBox = QVBoxLayout()
        gridBox = QGridLayout()
        gridBox.setSpacing(8)
        gridBox.addWidget(identLabel, 1, 0)
        gridBox.addWidget(self.IdentEdit, 1, 1)
        gridBox.addWidget(nameLabel, 2, 0)
        gridBox.addWidget(self.NameEdit, 2, 1)
        gridBox.addWidget(codeLabel, 3, 0)
        gridBox.addWidget(self.CodeEdit, 3, 1)
        gridBox.addWidget(ipAddLabel, 4, 0)
        gridBox.addWidget(self.IPAddEdit, 4, 1)
        gridBox.addWidget(regionLabel_1, 5, 0)
        gridBox.addWidget(self.RegionEdit_1, 5, 1)
        gridBox.addWidget(regionLabel_2, 6, 0)
        gridBox.addWidget(self.RegionEdit_2, 6, 1)
        gridBox.addWidget(typeLabel, 7, 0)
        gridBox.addWidget(self.TypeComboEdit, 7, 1)

        hBox.addWidget(regButton)
        hBox.addWidget(self.viewButton)
        hBox.addWidget(exitButton)

        vBox.addLayout(gridBox)
        vBox.addLayout(hBox)

        self.setLayout(vBox)
        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('개별장비등록')

    def SetInitText(self):
        self.ClearText()

        self.IdentEdit.setPlaceholderText('V5.2 or MGID')
        self.IdentEdit.setFocus()
        self.IdentEdit.returnPressed.connect(self.NameEdit.setFocus)
        self.NameEdit.setPlaceholderText('장비 이름(포항SYS1)')
        self.NameEdit.returnPressed.connect(self.CodeEdit.setFocus)
        self.CodeEdit.setPlaceholderText('장비 CallCode')
        self.CodeEdit.returnPressed.connect(self.IPAddEdit.setFocus)
        self.IPAddEdit.setPlaceholderText('장비 IP Address')
        self.IPAddEdit.returnPressed.connect(self.RegionEdit_1.setFocus)
        self.RegionEdit_1.setPlaceholderText('모국 입력')
        self.RegionEdit_1.returnPressed.connect(self.RegionEdit_2.setFocus)
        self.RegionEdit_2.setPlaceholderText('자국 아닐 경우 빈칸')
        self.RegionEdit_2.returnPressed.connect(self.TypeComboEdit.setFocus)

        typeList = ['ANY_LAG', 'ANY_LLS', 'Linux_1', 'Linux_2', 'Linux_3']

        comboModel = UserModel(typeList)
        self.TypeComboEdit.setModel(comboModel)

    def ClearText(self):
        self.IdentEdit.clear()
        self.NameEdit.clear()
        self.CodeEdit.clear()
        self.IPAddEdit.clear()
        self.RegionEdit_1.clear()
        self.RegionEdit_2.clear()

    def SaveDeviceInfo(self):

        nameDatabase_ = 'deviceList.db'
        saveRecord = controlDatabase.DeviceDataBase()

        infoList_ = [self.IdentEdit.text(), self.NameEdit.text(), self.CodeEdit.text(), self.IPAddEdit.text(),
                     self.RegionEdit_1.text(), self.RegionEdit_2.text(), self.TypeComboEdit.currentText()]

        saveRecord.OpenDB(nameDatabase_)
        saveRecord.SaveData(infoList_)
        saveRecord.CloseDB()

        if saveRecord.ErrorOfThis:
            QMessageBox.warning(self, "경보창", saveRecord.ErrorOfThis)
            self.IdentEdit.setFocus()

    def ViewDeviceInfo(self):

        nameDatabase_ = 'deviceList.db'
        viewRecord = controlDatabase.DeviceDataBase()
        viewRecord.OpenDB(nameDatabase_)
        allRecords = viewRecord.ViewAllData()
        viewRecord.CloseDB()
        if viewRecord.ErrorOfThis:
            QMessageBox.warning(self, "경보창", viewRecord.ErrorOfThis)
        else:
            for record in allRecords:
                print(record)

class UserModel(QStandardItemModel):
    def __init__(self, data=None, parent=None):
        QStandardItemModel.__init__(self, parent)
        for i, d in enumerate(data):
            self.setItem(i, 0, QStandardItem(d))

    def data(self, QModelIndex, role=None):
        data = self.itemData(QModelIndex)
        if role == Qt.DisplayRole:
            return "%s" % (data[role])
        elif role == Qt.UserRole:
            print(data[role])
        return QVariant()
