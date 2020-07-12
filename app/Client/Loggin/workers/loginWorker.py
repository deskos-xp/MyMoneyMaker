from PyQt5.QtCore import QObject,QThread,QThreadPool,QRunnable,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget
import os,sys,json,ast,requests
from ...MainWindow.default_fields import *

class loginWorkerSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasUser:pyqtSignal=pyqtSignal(object)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    session:requests.Session=requests.Session()
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class loginWorker(QRunnable):
    def __init__(self,auth):
        super(loginWorker,self).__init__()
        self.signals=loginWorkerSignals()
        self.auth=auth

    def run(self):
        try:
            j=dict(uname=self.auth.get("username"))
            uri="{host}/user/get".format(**dict(host=self.auth.get('host')))
            response=self.signals.session.post(uri,auth=(self.auth.get("username"),self.auth.get("password")),json=j,verify=verify(self.auth.get('host'))[0])
            self.signals.hasResponse.emit(response)
            Json=response.json()
            stat=Json.get("status")
            user=Json.get(stat)
            if user:
                self.signals.hasUser.emit(user)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
