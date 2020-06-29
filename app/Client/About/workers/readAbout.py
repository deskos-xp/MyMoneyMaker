from PyQt5.QtCore import QObject,QRunnable,QThreadPool,pyqtSignal,pyqtSlot
import os,sys,json
from pathlib import Path

class readAboutSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasAbout:pyqtSignal=pyqtSignal(dict)

    @pyqtSlot()
    def kill(self):
        self.killMe=True

class readAbout(QRunnable):
    def __init__(self,config:Path):
        super(readAbout,self).__init__()
        self.config=config
        self.signals=readAboutSignals()

    def run(self):
        try:
            d=dict()
            with open(self.config,"r") as fd:
                d=json.load(fd)
                #print(d)
            self.signals.hasAbout.emit(d)
        except Exception as e:
            print(e)
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
