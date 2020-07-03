from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QFileDialog
import os,sys,json
from pathlib import Path

from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import TableModel,TableModelEnum
from ..MainWindow.ModelDelegates import *
from .workers.readServerConfig import readServerConfig
from .workers.saveServerConfig import saveServerConfig
import time
from Server.config.Config import server_config

class ServerSettings(QDialog):
    def __init__(self,config_path:Path,parent):
        super(ServerSettings,self).__init__()
        self.config_path=config_path
        self.parent=parent
        self.dialog=QDialog(parent)
        uic.loadUi("Client/MainWindow/forms/server_settings.ui",self.dialog)

        self.conf_reader=readServerConfig(server_config())
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

        def userAcceptsChanges():      
            saver=saveServerConfig(self.dialog,server_config(),self.model.item)
            saver.signals.finished.connect(lambda:print("finished saving server... you need to restart the server"))
            #need a serverNeedsRestart signal
            saver.signals.hasError.connect(lambda x:print(x,"error"))
            QThreadPool.globalInstance().start(saver)
            
            print(self.model.item)
            
        self.dialog.confirm.accepted.connect(userAcceptsChanges)

        self.dialog.show()


    def browse_dir(self):
        b=QFileDialog.getExistingDirectory(self,"Select a Directory")
        if b:
            return b

    def browse_save(self):
        b=QFileDialog.getSaveFileName(self,"Where to save Log","","LOG/log (*.log);;All Files(*)",options=QFileDialog.DontUseNativeDialog)
        if b and len(b) > 0:
            return b[0]

    def setDelegates(self):
        for num,key in enumerate(self.model.item.keys()):
            if key in ["TESTING","FLASK_DEBUG","SQLALCHEMY_TRACK_MODIFICATIONS","NEED_ADMIN","USER_ENABLE_EMAIL","USER_ENABLE_USERNAME"]:
                self.dialog.editor.setItemDelegateForRow(num,CheckBoxDelegate(self.dialog))
            elif key in ['MAX_CONTENT_LENGTH']:
                self.dialog.editor.setItemDelegateForRow(num,SpinBoxDelegate(self.dialog))
            elif key in ['UPLOAD_FOLDER','LOG']:
                if key  == 'UPLOAD_FOLDER':
                    cmd=self.browse_dir
                else:
                    cmd=self.browse_save
                self.dialog.editor.setItemDelegateForRow(num,ButtonDelegate(self.dialog,cmd))
            elif key == "MESSAGING_PASSWORD":
                self.dialog.editor.setItemDelegateForRow(num,TextEditDelegate(self.dialog,password=True))
                #from PyQt5.QtWidgets import QTableView
                
            else:
                self.dialog.editor.setItemDelegateForRow(num,TextEditDelegate(self.dialog))
            
