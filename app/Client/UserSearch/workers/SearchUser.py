from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json,requests
import enum

class SUE(enum.Enum):
    limit={'key':'limit','value':10}
    page={'key':'page','value':0}

class SearchUserSignals(QObject):
    killMe:bool=False
    session:requests.Session=requests.Session()
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasResponse:pyqtSignal=pyqtSignal(requests.Response)
    hasUsers:pyqtSignal=pyqtSignal(list)

    @pyqtSlot()
    def kill(self):
        self.killMe=True
        self.session.close()

class SearchUser(QRunnable):
    def __init__(self,auth:dict,fields:dict):
        super(SearchUser,self).__init__()
        self.auth=auth
        self.fields=fields
        self.signals=SearchUserSignals()

    def run(self):
        try:
            addr="{host}/user/get".format(**self.auth)
            auth=(
                self.auth.get("uname"),
                self.auth.get("password")
                    )
            print(addr,"address "*10)
            print(self.fields,'data'*10)
            for k in ['page','limit']:
                if k not in self.fields.keys():
                    self.fields[k]=SUE.__dict__[k].value.get('value')
            print(auth,"auth"*10)
            response=self.signals.session.post(addr,auth=auth,json=self.fields)
            self.signals.hasResponse.emit(response)
            if response.status_code ==200:
                j=response.json()
                stat=j.get("status")
                users=j.get(stat)
                self.signals.hasUsers.emit(users)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
