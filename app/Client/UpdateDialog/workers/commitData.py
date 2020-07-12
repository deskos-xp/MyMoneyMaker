from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
import os,sys,json,requests
from PyQt5.QtWidgets import QWidget
from ...MainWindow.default_fields import *

class commitDataSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    finished:pyqtSignal=pyqtSignal()

    @pyqtSlot()
    def kill(self):
        self.session.close()
        self.killMe=True

class commitData(QRunnable):
    def __init__(self,auth,data):
        self.data=data
        self.auth=auth
        self.signals=commitDataSignals()
        super(commitData,self).__init__()

    def run(self):
        try:
            addr="{host}/saved/update/{id}".format(**dict(host=self.auth.get('host'),id=self.data.get("id")))
            auth=(
                self.auth.get("uname"),
                self.auth.get("password")
            )
            #del unuseable keys from data
            print(addr,"commitData address"*5)
            response=self.signals.session.post(addr,auth=auth,json=self.data,verify=verify(self.auth.get('host'))[0])
            print(response,"commitData "*10)
            self.signals.hasResponse.emit(response)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
