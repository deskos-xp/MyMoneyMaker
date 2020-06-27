import os,sys,json
from pathlib import Path

from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot

class RememberSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasUser:pyqtSignal=pyqtSignal(dict)

    @pyqtSlot()
    def kill(self):
        self.killMe=True

class Remember(QRunnable):
    def __init__(self,parent,config:Path):
        self.user:dict=dict()
        self.config=config
        self.parent=parent
        self.signals=RememberSignals()
        super(Remember,self).__init__()

    def run(self):
        try:
            with open(self.config,"r") as fd:
                self.user=json.load(fd)
            self.signals.hasUser.emit(self.user)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()

