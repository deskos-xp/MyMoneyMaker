from PyQt5 import uic
from PyQt5.QtCore import QThreadPool,QThread,QObject,QRunnable,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QTableView,QLabel,QDialogButtonBox
import json,os,sys
from pathlib import Path
from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import *
from .workers.readAbout import readAbout
from .workers.readIcon import readIcon
class About(QDialog):
    def __init__(self,parent):
        super(About,self).__init__()
        self.parent=parent
        self.gui=QDialog(parent)
        uic.loadUi("Client/MainWindow/forms/about.ui",self.gui)

        self.model=TableModel(item=dict(),ReadOnly=TableModelEnum.READONLY)

        self.gui.view.setModel(self.model)
        prep_table(self.gui.view)
        #getpixmap worker
        self.readAbout=readAbout(Path("Client/MainWindow/about.json"))
        self.readAbout.signals.finished.connect(lambda:print("finished reading about.json"))
        self.readAbout.signals.hasError.connect(lambda x:print(x))
        
        @pyqtSlot(dict)
        def update_about(data):
            #print(data,"update about"*3)
            self.model.load_data(data,re=True)
            icon=Path("Client/MainWindow") / Path(data.get("logo"))
            self.readIcon=readIcon(icon)
            self.readIcon.signals.hasBytesIO.connect(lambda x:print(x))
            self.readIcon.signals.hasImage.connect(lambda x:print(x))
            self.readIcon.signals.hasPixmap.connect(self.gui.logo.setPixmap)
            self.readIcon.signals.hasError.connect(lambda x:print(x))
            self.readIcon.signals.finished.connect(lambda : print("finished reading icon"))
            QThreadPool.globalInstance().start(self.readIcon)
        
        self.readAbout.signals.hasAbout.connect(update_about)
        QThreadPool.globalInstance().start(self.readAbout)

        self.gui.show()


