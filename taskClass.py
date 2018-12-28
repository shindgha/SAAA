
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import sys
import controlDatabase
import telnetClass

class TaskThread(QThread):
    taskFinished = pyqtSignal()
    changeProcBarvalue = pyqtSignal(int)

    def __init__(self, itemList_):
        QThread.__init__(self)

        self.itemList = itemList_
        self.isRunning = False
        self.isWaiting = False
        self.sumCnt = len(self.itemList)
        self.currentCnt = 0
        self.resultData = {}

    def GetdevProperty(self, devType_):
        devType = devType_
        nameDatabase = 'deviceList.db'
        getDataBase = controlDatabase.DeviceDataBase()
        getDataBase.OpenDB(nameDatabase)
        getRecord = getDataBase.GetDevProperty(devType)
        getDataBase.CloseDB()
        return getRecord

    def MarkOKIconOnItem(self, item_):
        item = item_
        iconPix = QPixmap("ic_thumb_up_black_24dp.png")
        icon = QIcon()
        icon.addPixmap(iconPix, QIcon.Normal, QIcon.Off)
        item.setIcon(6, icon)

    def MarkNOKIconOnItem(self, item_):
        item = item_
        iconPix = QPixmap("ic_thumb_down_black_24dp.png")
        icon = QIcon()
        icon.addPixmap(iconPix, QIcon.Normal, QIcon.Off)
        item.setIcon(6, icon)

    def ConnectDevAndGetAlramData(self, item_):
        item = item_
        devIP = item.text(2)
        devID = item.text(0)
        devType = item.text(3)
        devProperty = self.GetdevProperty(devType)
        tn = telnetClass.TelnetCilent()
        for dev in devProperty:
            cmdList = dev[5].split(',')
            tn.SetHostIPAdress(devIP, devID)
            tn.SetLoginPrompt(dev[1], dev[2])
            tn.SetUserNameAndPwd(dev[3], dev[4])
            print(tn.ConnTelnetToHost())
            if tn.ConnTelnetToHost():
                tn.LoginAndExecCommand(devType, cmdList)

        return tn.resultDictText

    def run(self):
        print(self.itemList)
        self.sumCnt = len(self.itemList)
        try:
            for item in self.itemList:
                listResult = self.ConnectDevAndGetAlramData(item)
                self.currentCnt += 1
                value = int(self.currentCnt / self.sumCnt * 100)
                self.changeProcBarvalue.emit(value)

                if listResult:
                    self.MarkOKIconOnItem(item)
                    self.taskFinished.emit()
                    self.resultData = listResult

                else:
                    self.MarkNOKIconOnItem(item)
                    self.taskFinished.emit()
                    self.resultData = {item.text(0) : "Fail"}

                while self.isWaiting:
                    self.sleep(1)
                if self.isRunning:
                    continue
                else:
                    self.isWaiting = True
        except Exception as err:
            print(err)
        self.exit()
