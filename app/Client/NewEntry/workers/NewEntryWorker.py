from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json,requests

from ...MainWindow.default_fields import *

class NewEntryWorkerSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)

    @pyqtSlot()
    def kill(self):
        self.session.close()
        self.killMe=True

class NewEntryWorker(QRunnable):
    def __init__(self,auth:dict,data:dict):
        self.data=data
        self.auth=auth
        self.signals=NewEntryWorkerSignals()

        super(NewEntryWorker,self).__init__()

    def run(self):
        try:
            self.data.__delitem__('id')
            addr="{host}/saved/new".format(**self.auth)
            auth=(
                self.auth.get("uname"),
                self.auth.get("password")
            )
            print(addr,auth,self.data)
            response=self.signals.session.post(addr,auth=auth,json=self.data,verify=verify(self.auth.get('host'))[0])
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
