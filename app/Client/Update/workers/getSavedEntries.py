from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QWidget
import os,sys,requests,json


class getSavedEntriesSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasData:pyqtSignal=pyqtSignal(list)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class getSavedEntries(QRunnable):
    def __init__(self,auth:dict,search_data):
        self.search_data=search_data
        self.auth=auth
        self.signals=getSavedEntriesSignals()
        super(getSavedEntries,self).__init__()

    def run(self):
        try:
            addr="{host}/saved/get".format(**self.auth)
            auth=(
                self.auth.get("uname"),
                self.auth.get("password")
            )
            response=self.signals.session.post(addr,json=self.search_data,auth=auth)
            self.signals.hasResponse.emit(response)
            j=response.json()
            data=j.get("status")
            data=j.get(data)
            if isinstance(data,list):
                self.signals.hasData.emit(data)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
