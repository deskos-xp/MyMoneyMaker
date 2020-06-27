from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json,requests,time

class ReviewLastSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasData:pyqtSignal=pyqtSignal(dict)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    session=requests.Session()
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class ReviewLast(QRunnable):
    def __init__(self,auth:dict):
        super(ReviewLast,self).__init__()
        self.auth=auth
        self.signals=ReviewLastSignals()

    def run(self):
        try:
            addr="{host}/saved/get/last".format(**dict(host=self.auth.get("host")))
            response=self.signals.session.get(addr,auth=(self.auth.get("uname"),self.auth.get("password")))
            self.signals.hasResponse.emit(response)
            if response.status_code == 200:
                data=response.json()
                a=data[data.get("status")]['date']
                if a == "":
                    data[data.get("status")]['date']=time.strftime("%m/%d/%Y",time.localtime())
                self.signals.hasData.emit(data)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
