from PyQt5.QtCore import QRunnable,QObject,QThread,QThreadPool,pyqtSlot,pyqtSignal
import os,sys,json
from PyQt5.QtGui import QPixmap,QImage
from pathlib import Path
from io import BytesIO
class readIconSignals(QObject):
    killMe:bool=False
    finished:pyqtSignal=pyqtSignal()
    hasError:pyqtSignal=pyqtSignal(Exception)
    hasImage:pyqtSignal=pyqtSignal(QImage)
    hasPixmap:pyqtSignal=pyqtSignal(QPixmap)
    hasBytesIO:pyqtSignal=pyqtSignal(BytesIO)

    @pyqtSlot()
    def kill(self):
        self.killMe=True

class readIcon(QRunnable):
    def __init__(self,path:Path):
        self.path=path
        self.signals=readIconSignals()
        super(readIcon,self).__init__()

    def run(self):
        try:
            bio=BytesIO()
            with open(self.path,"rb") as fd:
                while True:
                    buf=fd.read(1024)
                    if not buf:
                        break
                    bio.write(buf)
            bio.seek(0)
            self.signals.hasBytesIO.emit(bio)
            img=QImage.fromData(bio.getvalue())
            self.signals.hasImage.emit(img)
            self.signals.hasPixmap.emit(QPixmap.fromImage(img))
        except Exception as e:
            self.signals.hasError.emit(e)
        self.signals.finished.emit()
