from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json
from pathlib import Path


class UserDialog(QDialog):
    def __init__(self,parent):
        self.parent=parent
        self.auth=parent.stacks['charting'].auth
        super(UserDialog,self).__init__()

        self.dialog=QDialog(parent)
        try:
            uic.loadUi("Client/MainWindow/forms/userdialog.ui",self.dialog)
        except:
            pass
        
        print(self.auth)
        self.dialog.show()
