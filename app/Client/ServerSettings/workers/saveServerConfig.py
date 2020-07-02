from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSlot,pyqtSignal
import os,sys,json
from pathlib import Path

class saveServerConfigSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    
    @pyqtSlot()
    def kill(self):
        self.killMe=True

class saveServerConfig(QRunnable):
    def __init__(self,parent,config_path:Path,new:dict):
        super(saveServerConfig,self).__init__()
        self.signals=saveServerConfigSignals()
        self.parent=parent
        self.config_path=config_path
        self.new=new
        
    def run(self):
        try:
            with open(self.config_path,"w") as fd:
                json.dump(self.new,fd)
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
