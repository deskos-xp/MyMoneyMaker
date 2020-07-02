from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QFileDialog
import os,sys,json
from pathlib import Path

from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import TableModel,TableModelEnum
from ..MainWindow.ModelDelegates import *
from .workers.readServerConfig import readServerConfig
import time

class ServerSettings(QDialog):
    def __init__(self,config_path:Path,parent):
        super(ServerSettings,self).__init__()
        self.config_path=config_path
        self.parent=parent
        self.dialog=QDialog(parent)
        uic.loadUi("Client/MainWindow/forms/server_settings.ui",self.dialog)

        self.conf_reader=readServerConfig("Server/config/env.json")
        self.conf_reader.signals.finished.connect(lambda : print("finished reading server config"))
        self.conf_reader.signals.hasError.connect(lambda x:print(x,"error"))

        @pyqtSlot(dict)
        def load(data):
            print(data)
            self.model.load_data(data,re=True)
            self.setDelegates()
        
        self.conf_reader.signals.hasConfig.connect(load)
        QThreadPool.globalInstance().start(self.conf_reader)

        self.model=TableModel(item=dict())
        self.dialog.editor.setModel(self.model)

        prep_table(self.dialog.editor)

        self.dialog.show()


    def browse_dir(self):
        b=QFileDialog.getExistingDirectory(self,"Select a Directory")
        if b:
            print(b)
            return b
        else:
            return "Browse"

    def setDelegates(self):
        for num,key in enumerate(self.model.item.keys()):
            if key in ["TESTING","FLASK_DEBUG","SQLALCHEMY_TRACK_MODIFICATIONS","NEED_ADMIN","USER_ENABLE_EMAIL","USER_ENABLE_USERNAME"]:
                self.dialog.editor.setItemDelegateForRow(num,CheckBoxDelegate(self.dialog))
            elif key in ['MAX_CONTENT_LENGTH']:
                self.dialog.editor.setItemDelegateForRow(num,SpinBoxDelegate(self.dialog))
            elif key in ['UPLOAD_FOLDER']:
                self.dialog.editor.setItemDelegateForRow(num,ButtonDelegate(self.dialog,self.browse_dir))
