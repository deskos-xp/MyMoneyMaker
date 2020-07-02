from PyQt5.QtCore import QObject,QRunnable,QThreadPool,QThread,pyqtSignal,pyqtSlot
import json,os,sys
from pathlib import Path

class readServerConfigSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasConfig:pyqtSignal=pyqtSignal(dict)

    @pyqtSlot()
    def kill(self):
        self.killMe=True


class readServerConfig(QRunnable):
    def __init__(self,config_path:Path):
        self.config_path=config_path
        self.signals=readServerConfigSignals()
        super(readServerConfig,self).__init__()

    def run(self):
        try:
            d=dict()
            with open(self.config_path,"r") as fd:
                d=json.load(fd)
                if not d:
                    raise Exception
                self.signals.hasConfig.emit(d)
                #print(d)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()

