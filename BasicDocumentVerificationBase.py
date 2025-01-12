import BasicDocumentVerification
import LogHelper
import datetime

def Run():
    LogHelper.PrintInfoLog("Basit doküman doğrulama süreci başladı.")
    startDate=datetime.datetime.now()
    BasicDocumentVerification.StartBasicDocumentVerification()
    endDate=datetime.datetime.now()
    LogHelper.PrintInfoLog("\n Basit doküman doğrulama süreci bitti. Toplam çalışma süresi: " + str(endDate-startDate))

Run()