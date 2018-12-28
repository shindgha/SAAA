class MakeItemData:
    def __init__(self):
        pass

    def MakeTreeTopLevelData_region(self, allRecords_):
        allRecords = allRecords_

        topList = []
        secondList = []
        thirdList = []
        tmpList = []

        for record in allRecords:
            if record[4] not in topList:
                topList.append(record[4])

        for record in allRecords:
            if record[5] not in tmpList:
                tmpList.append(record[5])
                secondList.append(('{}'.format(record[4]), '{}'.format(record[5])))

        for record in allRecords:
            tmpTuple = (record[4],record[5],record[1],record[0],record[6])
            thirdList.append(tmpTuple)

        return topList, secondList, thirdList