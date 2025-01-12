import datetime

def GetCurrentDatetime():
    return datetime.datetime.now()

def GetDifferenceDate(endDate,startDate):
    return str(endDate-startDate)