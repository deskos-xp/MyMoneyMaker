from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
import requests,os,sys,json
from ...MainWindow.default_fields import *

class DeleteUserSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class DeleteUser(QRunnable):
    def __init__(self,auth,user_id):
        super(DeleteUser,self).__init__()
        self.auth=auth
        self.user_id=user_id
        self.signals=DeleteUserSignals()

    def run(self):
        try:
            addr="{host}/user/delete/{id}".format(**dict(host=self.auth.get("host"),id=self.user_id))
            auth=(
                    self.auth.get("uname"),
                    self.auth.get("password")
                    )
            response=self.signals.session.delete(addr,auth=auth,verify=verify(self.auth.get('host'))[0])
            self.signals.hasResponse.emit(response)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()

