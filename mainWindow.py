import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import registeDevInfo
import controlDatabase
import otherWidgets
import makeItemData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Simple AGW Alarm Analyzer'
        self.left = 400
        self.top = 200
        self.width = 800
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        regSysMenu = mainMenu.addMenu('장비등록')
        analyMenu = mainMenu.addMenu('장비점검')
        viewMenu = mainMenu.addMenu('결과보기')
        helpMenu = mainMenu.addMenu('도움말')

        eachSysRegSubMenu = QAction(QIcon('exit24.png'), '개별장비등록', self)
        eachSysRegSubMenu.setShortcut('Ctrl+R')
        eachSysRegSubMenu.setStatusTip('한개의 장비를 등록 합니다')
        eachSysRegSubMenu.triggered.connect(self.on_eachSysRegSubMenu_clicked)
        regSysMenu.addAction(eachSysRegSubMenu)

        allSysRegSubMenu = QAction(QIcon('exit24.png'), '일괄장비등록', self)
        allSysRegSubMenu.setShortcut('Ctrl+A')
        allSysRegSubMenu.setStatusTip('여러개의 장비를 등록 합니다')
        allSysRegSubMenu.triggered.connect(self.on_allSysRegSubMenu_clicked)
        regSysMenu.addAction(allSysRegSubMenu)

        viewSysRegSubMenu = QAction(QIcon('exit24.png'), '등록장비보기', self)
        viewSysRegSubMenu.setShortcut('Ctrl+V')
        viewSysRegSubMenu.setStatusTip('등록된 장비를 볼 수 있습니다')
        viewSysRegSubMenu.triggered.connect(self.on_ViewDeviceInfo)
        regSysMenu.addAction(viewSysRegSubMenu)

        delSysRegSubMenu = QAction(QIcon('exit24.png'), '등록정보삭제', self)
        delSysRegSubMenu.setShortcut('Ctrl+D')
        delSysRegSubMenu.setStatusTip('등록된 장비를 정보를 삭제 합니다')
        delSysRegSubMenu.triggered.connect(self.on_deleteDeviceInfo)
        regSysMenu.addAction(delSysRegSubMenu)

        updateSysRegSubMenu = QAction(QIcon('exit24.png'), '자료전체삭제', self)
        updateSysRegSubMenu.setShortcut('Ctrl+U')
        updateSysRegSubMenu.setStatusTip('Databse Table 자료 전체 삭제 합니다')
        updateSysRegSubMenu.triggered.connect(self.on_allDataDeleteSubMenu_clicked)
        regSysMenu.addAction(updateSysRegSubMenu)

        exitSubMenu = QAction(QIcon('exit24.png'), '종료', self)
        exitSubMenu.setShortcut('Ctrl+Q')
        exitSubMenu.setStatusTip('프로그램을 종료 합니다')
        exitSubMenu.triggered.connect(self.close)
        regSysMenu.addAction(exitSubMenu)

        allSysAnalySubMenu = QAction(QIcon('exit24.png'), '전체정비점검', self)
        allSysAnalySubMenu.setShortcut('Ctrl+A')
        allSysAnalySubMenu.setStatusTip('한개의 장비를 등록 합니다')
        allSysAnalySubMenu.triggered.connect(self.on_allSysAnalySubMenu_clicked)
        analyMenu.addAction(allSysAnalySubMenu)

        eachSysAnalySubMenu = QAction(QIcon('exit24.png'), '개별장비점검', self)
        eachSysAnalySubMenu.setShortcut('Ctrl+A')
        eachSysAnalySubMenu.setStatusTip('한개의 장비를 등록 합니다')
        eachSysAnalySubMenu.triggered.connect(self.on_eachSysAnalySubMenu_clicked)
        analyMenu.addAction(eachSysAnalySubMenu)

        self.show()
        self.startWindow()

    def startWindow(self):
        self.on_ViewDeviceInfo()

    def on_eachSysRegSubMenu_clicked(self):
        regDevice = registeDevInfo.RegisteDeviceDialog()
        regDevice.viewButton.pressed.connect(self.on_ViewDeviceInfo)
        regDevice.exec_()

    def on_allSysRegSubMenu_clicked(self):
        openFileName, _ = QFileDialog.getOpenFileName(None, 'Open file', "",
                                                  'All Files (*);;Python Files (*.py);; Data files(*.dat)')
        try:
            if openFileName:
                openFile = open(openFileName, 'rt', encoding='utf-8')
                records = openFile.readlines()

                nameDatabase_ = 'deviceList.db'
                saveRecord = controlDatabase.DeviceDataBase()
                saveRecord.OpenDB(nameDatabase_)
                viewList = []

                for line in records:
                    tmp = line.rstrip('\n')
                    record = [tmp.split(',')]
                    for field in record:
                        saveRecord.SaveData(field)
                        viewList.append(field)
                    if saveRecord.ErrorOfThis:
                        QMessageBox.warning(self, "경보창", "에러 발생 : {} : ".format(saveRecord.ErrorOfThis))
                        saveRecord.ErrorOfThis = ""
                openFile.close()
                saveRecord.CloseDB()

                viewWidget = otherWidgets.ViewWidget(viewList)
                self.setCentralWidget(viewWidget)
        except Exception as e:
            QMessageBox.warning(self, "경보창", "에러 발생 : {}".format(e))
            self.startWindow()


    def on_ViewDeviceInfo(self):
        try:
            nameDatabase = 'deviceList.db'
            viewRecord = controlDatabase.DeviceDataBase()
            viewRecord.OpenDB(nameDatabase)
            allRecords = viewRecord.ViewAllData()
            viewRecord.CloseDB()

            if viewRecord.ErrorOfThis:
                QMessageBox.warning(self, "경보창", "{} : ".format(viewRecord.ErrorOfThis))
                viewRecord.ErrorOfThis = ""

            viewWidget = otherWidgets.ViewWidget(allRecords)
            self.setCentralWidget(viewWidget)
        except Exception as err:
            print(err)
            if viewRecord.ErrorOfThis:
                QMessageBox.warning(self, "경보창", "{} : ".format(viewRecord.ErrorOfThis))
                viewRecord.ErrorOfThis = ""



    def on_deleteDeviceInfo(self):
        deleteText_, ok = QInputDialog.getText(self, '장비정보삭제', '장비 ID을 입력하세요.')

        if ok:
            nameDatabase_ = 'deviceList.db'
            deleteRecord = controlDatabase.DeviceDataBase()
            deleteRecord.OpenDB(nameDatabase_)
            deleteRecord.DelectData(str(deleteText_))
            deleteRecord.CloseDB()


            if deleteRecord.ErrorOfThis:
                QMessageBox.warning(self, '경보창', deleteRecord.ErrorOfThis)
                deleteRecord.ErrorOfThis = ''
            else:
                QMessageBox.warning(self, '알림창', "장비ID {}는 삭제 되었습니다".format(deleteText_))

    def on_allDataDeleteSubMenu_clicked(self):
        nameDatabase_ = 'deviceList.db'
        deleteAllRecord = controlDatabase.DeviceDataBase()
        deleteAllRecord.OpenDB(nameDatabase_)
        deleteAllRecord.DeleteAllData('deviceInfo')
        deleteAllRecord.CloseDB()

        if deleteAllRecord.ErrorOfThis:
            QMessageBox.warning(self, '경보창', deleteAllRecord.ErrorOfThis)
            deleteAllRecord.ErrorOfThis = ''
        else:
            QMessageBox.warning(self, '알림창', '장비 데이타가 모두 삭제되었습니다')
            self.startWindow()

    def on_eachSysAnalySubMenu_clicked(self):
        nameDatabase = 'deviceList.db'
        viewRecord = controlDatabase.DeviceDataBase()
        viewRecord.OpenDB(nameDatabase)
        allRecords = viewRecord.ViewAllData()
        viewRecord.CloseDB()
        if viewRecord.ErrorOfThis:
            QMessageBox.warning(self, "경보창", "{} : ".format(viewRecord.ErrorOfThis))
            viewRecord.ErrorOfThis = ""
        else:
            ItemData = makeItemData.MakeItemData()
            topLevel, secondLevel, thirdLevel = ItemData.MakeTreeTopLevelData_region(allRecords)

            userTreeWidget = otherWidgets.TreeWidget()
            userTreeWidget.CreateTree(topLevel, secondLevel, thirdLevel)

            self.setCentralWidget(userTreeWidget)

    def on_allSysAnalySubMenu_clicked(self):
        try:
            nameDatabase = 'deviceList.db'
            analyRecord = controlDatabase.DeviceDataBase()
            analyRecord.OpenDB(nameDatabase)
            allRecords = analyRecord.ViewAllData()
            analyRecord.CloseDB()
        except Exception as err:
            if analyRecord.ErrorOfThis:
                QMessageBox.warning(self, "경보창", "{} : ".format(analyRecord.ErrorOfThis))
                analyRecord.ErrorOfThis = ""
        try:
            analyWidget = otherWidgets.AnalyAllWidget(allRecords)
            analyWidget.CreateAnalyTree()
            analyWidget.SetInitIconTree()
            self.setCentralWidget(analyWidget)

            analyWidget.analyFinished.connect(self.on_ViewDeviceInfo)
        except Exceptionas as err:
            print(err)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWndow_ = MainWindow()
    sys.exit(app.exec_())