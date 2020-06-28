from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal
import os,sys,json,requests

class getEntriesSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasEntries:pyqtSignal=pyqtSignal(dict)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasError:pyqtSignal=pyqtSignal(Exception)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class getEntries(QRunnable):
    def __init__(self,auth):
        super(getEntries,self).__init__()
        self.auth=auth
        self.signals=getEntriesSignals()

    def run(self):
        try:
            print(self.auth,"getEntries"*10)
            addr="{host}/saved/get".format(**self.auth)
            auth=(
                    self.auth.get("uname"),
                    self.auth.get("password")
                    )
            response=self.signals.session.post(addr,auth=auth,json=dict(page=0,limit=sys.maxsize))
            self.signals.hasResponse.emit(response)
            if response.json():
                self.signals.hasEntries.emit(response.json())
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
