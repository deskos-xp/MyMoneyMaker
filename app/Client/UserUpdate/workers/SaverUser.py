from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
import os,sys,json,requests


class SaveUserSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SaveUser(QRunnable):
    def __init__(self,auth:dict,user:dict):
        self.auth=auth
        self.user=user
        self.signals=SaveUserSignals()
        super(SaveUser,self).__init__()

    def run(self):
        try:
            addr="{host}/user/update/{id}".format(**dict(id=self.user.get("id"),host=self.auth.get("host")))
            auth=(
                    self.auth.get("uname"),
                    self.auth.get("password")
                    )
            response=self.signals.session.post(addr,auth=auth,json=self.user)
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
