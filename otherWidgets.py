from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import taskClass
import controlDatabase


class ViewWidget(QWidget):
    ID, NAME, CODE, IP, REGION_1, REGION_2, TYPE = range(7)

    def __init__(self, viewList_):
        super().__init__()
        self.viewList = viewList_
        self.initUI()

    def initUI(self):
        self.dataGroupBox = QGroupBox("등록장비 리스트")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        self.userModel = self.createViewModel(self)
        self.dataView.setModel(self.userModel)

        for data in self.viewList:
            self.AddViewData(data)

    def createViewModel(self, parent_):
        parent = parent_
        model = QStandardItemModel(0, 7, parent)
        model.setHeaderData(self.ID, Qt.Horizontal, "장비ID")
        model.setHeaderData(self.NAME, Qt.Horizontal, "장비명칭")
        model.setHeaderData(self.CODE, Qt.Horizontal, "장비별칭")
        model.setHeaderData(self.IP, Qt.Horizontal, "장비IP")
        model.setHeaderData(self.REGION_1, Qt.Horizontal, "설치모국")
        model.setHeaderData(self.REGION_2, Qt.Horizontal, "설치자국")
        model.setHeaderData(self.TYPE, Qt.Horizontal, "장비종류")

        return model

    def AddViewData(self, dataList_):
        dataList = dataList_
        self.userModel.insertRow(0)
        self.userModel.setData(self.userModel.index(0, self.ID), dataList[0])
        self.userModel.setData(self.userModel.index(0, self.NAME), dataList[1])
        self.userModel.setData(self.userModel.index(0, self.CODE), dataList[2])
        self.userModel.setData(self.userModel.index(0, self.IP), dataList[3])
        self.userModel.setData(self.userModel.index(0, self.REGION_1), dataList[4])
        self.userModel.setData(self.userModel.index(0, self.REGION_2), dataList[5])
        self.userModel.setData(self.userModel.index(0, self.TYPE), dataList[6])


class AnalyAllWidget(QWidget):
    analyFinished = pyqtSignal()

    def __init__(self, allTreeData_):
        QWidget.__init__(self)
        self.allTreeData = allTreeData_
        #self.f = open("tmpResult.txt", "w")
        self.ItemList = []
        try:
            nameDatabase = 'resultData.db'
            saveResult = controlDatabase.DeviceDataBase()
            saveResult.OpenDB(nameDatabase)


        except Exception as err:
            if analyRecord.ErrorOfThis:
                QMessageBox.warning(self, "경보창", "{} : ".format(analyRecord.ErrorOfThis))
                analyRecord.ErrorOfThis = ""


        self.startButton = QPushButton('점검시작')
        self.startButton.setStyleSheet("background-color: green")
        self.startButton.pressed.connect(self.on_startButton_pressed)

        self.pauseButton = QPushButton('점검중지')
        self.pauseButton.setStyleSheet("background-color: green")
        self.pauseButton.pressed.connect(self.on_pauseButton_pressed)

        exitButton = QPushButton('점검종료')
        exitButton.setStyleSheet("background-color: green")
        exitButton.pressed.connect(self.on_exitButton_pressed)

        self.procBar = QProgressBar()

        self.treeGroupBox = QGroupBox("점검장비 리스트")

        self.treeWidget = QTreeWidget(self)
        self.treeWidget.resize(700, 400)
        self.treeWidget.setColumnCount(6)
        self.treeWidget.setColumnWidth(0, 100)
        self.treeWidget.setHeaderLabels(['장비ID', '장비명칭', '장비IP', '장비종류',
                                         '설치위치1', '설치위치2', '점검상태'])

        treeLayout = QHBoxLayout()
        treeLayout.addWidget(self.treeWidget)
        self.treeGroupBox.setLayout(treeLayout)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.startButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(exitButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.procBar)
        mainLayout.addWidget(self.treeGroupBox)
        self.setLayout(mainLayout)

        self.myTask = taskClass.TaskThread(self.ItemList)
        self.myTask.taskFinished.connect(self.on_updataSelfWidget)
        self.myTask.finished.connect(self.on_TaskFinished)
        self.myTask.changeProcBarvalue.connect(self.procBar.setValue)
        print('초기화')

    def CreateAnalyTree(self):
        try:
            for item in self.allTreeData:
                treeRoot = QTreeWidgetItem([item[0], item[1], item[3], item[6], item[4], item[5]])
                self.treeWidget.addTopLevelItem(treeRoot)
                self.ItemList.append(treeRoot)
        except Exception as err:
            print(err)

    def SetInitIconTree(self):
        for item in self.ItemList:
            iconPix = QPixmap("ic_visibility_off_grey600_24dp.png")
            icon = QIcon()
            icon.addPixmap(iconPix, QIcon.Normal, QIcon.Off)
            item.setIcon(6, icon)

    def on_startButton_pressed(self):
        if self.myTask.isWaiting:
            pass
        else:
            self.SetInitIconTree()

        self.myTask.isRunning = True
        self.myTask.isWaiting = False
        self.myTask.start()
        self.pauseButton.setStyleSheet("background-color: green")
        self.startButton.setStyleSheet("background-color: red")
        self.startButton.setText('점검중')
        self.pauseButton.setText('점검정지')

    def on_pauseButton_pressed(self):
        self.myTask.isWaiting = True
        self.startButton.setText('재시작')
        self.pauseButton.setText('정지중')
        self.pauseButton.setStyleSheet("background-color: red")
        self.startButton.setStyleSheet("background-color: green")

    def on_exitButton_pressed(self):
        if self.myTask.isRunning:
            self.myTask.isRunning = False
        else:
            if self.myTask.isWaiting:
                self.myTask.isWaiting = False
                self.myTask.isRunning = False
        self.analyFinished.emit()

    def on_updataSelfWidget(self):
        print('Signal OK')
        for key, val in self.myTask.resultData.items():
            print(key)
            print(val)
            '''
            a = u''.join((key)).encode('utf-8')
            b = u''.join(val).encode('utf-8')

            self.f.write(str(a))
            self.f.write(str(b))
            '''

        self.myTask.resultData = {}
        self.treeWidget.setFocus()
        self.treeGroupBox.setFocus()

    def on_TaskFinished(self):
        self.startButton.setText('점검시작')
        self.startButton.setStyleSheet("background-color: green")
        QMessageBox.about(self, '작업완료', '전제분석 작업 완료')


class TreeWidget(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

    def CreateTree(self, topLevel_, secondLevel_, thirdLevel_):
        try:
            treeWidget = QTreeWidget(self)
            treeWidget.resize(480, 640)
            treeWidget.setColumnWidth(0, 150)
            treeWidget.setColumnCount(3)
            treeWidget.setHeaderLabels(['설치지역', '장비ID', '장비종류'])
            treeWidget.itemDoubleClicked.connect(self.on_itemDoubleClicked)

            itemLevel_top = topLevel_
            itemLevel_2nd = secondLevel_
            itemLevel_3th = thirdLevel_

            for item_1 in itemLevel_top:
                levelOne = QTreeWidgetItem([item_1])
                treeWidget.addTopLevelItem(levelOne)
                for (item_2_1, item_2_2) in itemLevel_2nd:
                    if item_1 == item_2_1:
                        levelTwo = QTreeWidgetItem([item_2_2])
                        # levelTwo.setExpanded(True)
                        levelOne.addChild(levelTwo)
                    for (col_1, col_2, col_3, col_4, col_5) in itemLevel_3th:
                        if item_1 == col_1 and item_2_2 == col_2:
                            levelTwo.addChild(QTreeWidgetItem([(col_3), (col_4), (col_5)]))
        except Exception as err:
            print(err)

    def on_itemDoubleClicked(self, item_, columnNo_):
        revItem = item_
        columnNo = columnNo_
        print(revItem.text(2))
        print(columnNo)


'''
nameDatabase = 'deviceList.db'
viewRecord = controlDatabase.DeviceDataBase()
viewRecord.OpenDB(nameDatabase)
allRecords = viewRecord.ViewAllData()
viewRecord.CloseDB()
'''
'''
allRecords = [('172.30.1.50', 'shindgha', '%passwdsy10%', '1864001'),
			  ('172.30.1.51', 'shindgha', '%passwdsy10%', '1864002'),
			  ('192.168.150.128', 'shindgha', '!passwd!', '1864003'),
			  ('172.30.1.50', 'shindgha', '%passwdsy10%', '1864002'),
			  ('172.30.1.51', 'shindgha', '%passwdsy10%', '1864002'),
			  ('192.168.150.128', 'shindgha', '!passwd!', '1864003'),
			  ('172.30.1.50', 'shindgha', '%passwdsy10%', '1864002'),
			  ('172.30.1.51', 'shindgha', '%passwdsy10%', '1864002'),
			  ('192.168.150.128', 'shindgha', '!passwd!', '1864003'),
			  ('172.30.1.50', 'shindgha', '%passwdsy10%', '1864002'),
			  ('172.30.1.51', 'shindgha', '%passwdsy10%', '1864002'),
			  ('192.168.150.128', 'shindgha', '!passwd!', '1864003')]
allCmdList = 'ls -al|cd /etc|ls -al|cd /tmp|ls -al'
cmdList = allCmdList.split('|')
hostList = []
resultText = []
for host in allRecords:
    hostIP = host[0]
    userName = host[1]
    passWord = host[2]
    devID = host[3]
    hostType = 'Linux'

    tn = TelnetCilent(hostIP, userName, passWord, devID)
    try:
        tn.ConnTelnetToHost()
    except:
        print('접속불가')
    if tn.connTelnet:
        tn.LoginToHost(hostType)
        tn.SendCommand(cmdList)
        time.sleep(1)
        resultText.append(tn.resultDictText)
    else:
        pass

for data in resultText:
    print(data)
'''
