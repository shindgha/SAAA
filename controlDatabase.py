from PyQt5.QtWidgets import QMessageBox
import sqlite3

class DeviceDataBase():
    def __init__(self):

        self.ErrorOfThis = ''
        print("Init DB")

    def SaveData(self, infoList_):
        infoList = infoList_
        try:
            sql = """insert into deviceInfo values (?, ?, ?, ?, ?, ?,?)"""
            self.cur.execute(sql,(infoList[0], infoList[1], infoList[2], infoList[3],
                                  infoList[4], infoList[5], infoList[6]))
            self.conn.commit()
            print("Save Data : {} ".format(infoList[0]))
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]
            print('Error')

    def SaveResultData(self, resultData_):
        resultData = resultData_
        for key, val in resultData.items():
            try:
                sql = """insert into  values (?, ?)"""
                self.cur.execute(sql,(key, val))
                self.conn.commit()
                print("Save Data : {} ".format(key))
            except sqlite3.Error as e:
                self.ErrorOfThis = e.args[0]
                print('Error')

    def DelectData(self, deleteDev_):
        deleteDev = deleteDev_
        try:
            sql = """select * from deviceInfo where ID=:ID"""
            self.cur.execute(sql,{"ID" : deleteDev})
            if self.cur.fetchall():
                sql = """delete from deviceInfo where ID=:ID"""
                self.cur.execute(sql,{"ID" : deleteDev})
                self.conn.commit()
                print("Delete Data")
            else:
                self.ErrorOfThis = '입력하신 ID를 확인 하세요'
                print('Error')
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]
            print('Error')

    def DeleteAllData(self, nameTable_):
        nameTable = nameTable_
        try:
            sql = 'delete from {}'.format(nameTable)
            self.cur.execute(sql)
            self.conn.commit()
            print("Deleted All Data")
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]
            print('Error')

    def ViewAllData(self):
        try:
            sql = 'select {} from '
            self.cur.execute("select * from deviceInfo")
            allRecords = self.cur.fetchall()
            if allRecords == [] :
                self.ErrorOfThis = '검색된 결과가 없습니다'
                return allRecords
            else:
                return allRecords
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]

    def GetDevProperty(self, devType_):
        devType = devType_
        try:
            sql = """select * from deviceType where Type=:Type"""
            self.cur.execute(sql,{"Type" : devType})
            allRecords = self.cur.fetchall()
            if allRecords == []:
                self.ErrorOfThis = '검색된 결과가 없습니다'
                return 0
            else:
                return allRecords
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]

    def GetDevInfoData(self, devIDdata_):
        devIDdata = devIDdata_
        try:
            sql = """select * from deviceInfo where ID=:ID"""
            self.cur.execute(sql, {"Type": devIDdata})
            if allRecords == []:
                self.ErrorOfThis = '검색된 결과가 없습니다'
                return allRecords
            else:
                return allRecords
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]

        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]

    def OpenDB(self, nameDatabase):
        try:
            self.conn = sqlite3.connect(nameDatabase)
            self.cur = self.conn.cursor()
            print('open DB')
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]

    def CloseDB(self):
        try:
            self.conn.close()
            print('close DB')
        except sqlite3.Error as e:
            self.ErrorOfThis = e.args[0]
