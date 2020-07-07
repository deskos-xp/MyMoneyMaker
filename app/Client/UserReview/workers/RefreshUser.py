from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget

import os,sys,json,requests


class RefreshUserSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasUser:pyqtSignal=pyqtSignal(dict)
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)

    @pyqtSlot()
    def kill(self):
        self.session.close()
        self.killMe=True

class RefreshUser(QRunnable):
    def __init__(self,auth:dict,user_id:int):
        self.auth=auth
        self.user_id=user_id
        self.signals=RefreshUserSignals()
        super(RefreshUser,self).__init__()

    def run(self):
        try:
            auth=(
                self.auth.get("uname"),
                self.auth.get("password")
                )
            addr="{host}/user/get/{id}".format(**dict(host=self.auth.get("host"),id=self.user_id))
            response=self.signals.session.get(addr,auth=auth)
            self.signals.hasResponse.emit(response)
            if response.status_code == 200:
                j=response.json()
                stat=j.get("status")
                user=j.get(stat)
                user['password']='xxxxxxxx'
                self.signals.hasUser.emit(user)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
