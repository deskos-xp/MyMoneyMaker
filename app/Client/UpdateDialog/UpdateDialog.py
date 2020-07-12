from PyQt5 import uic
from PyQt5.QtCore import QObject,QThread,QRunnable,QThreadPool,pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QErrorMessage
import os,sys,json,requests

from ..MainWindow.default_fields import *
from ..MainWindow.TableModel_editor import TableModel_editor as TableModel,TableModel_editorEnum as TableModelEnum
from ..MainWindow.ModelDelegates import *
from .workers.commitData import commitData

class UpdateDialog(QDialog):
    updateTab:pyqtSignal=pyqtSignal()
    def __init__(self,auth,data):
        self.auth=auth
        self.data=data
        super(UpdateDialog,self).__init__()

        self.dialog=QDialog()
        uic.loadUi("Client/MainWindow/forms/update_dialog.ui",self.dialog)
        self.dialog.setWindowTitle("Update")
        self.model=TableModel(item=data)
        self.dialog.editor.setModel(self.model)
        prep_table(self.dialog.editor)
        for num,k in enumerate(self.model.item.keys()):
            if k in currency().keys():
                if k == 'id':
                    pass
                elif k == 'date':
                    self.dialog.editor.setItemDelegateForRow(num,DateEditDelegate(self.dialog.editor))
                else:
                    self.dialog.editor.setItemDelegateForRow(num,SpinBoxDelegate(self.dialog.editor))
                
        self.dialog.rejected.connect(lambda : print("user rejected changes"))
        self.dialog.confirm.rejected.connect(lambda: print("user rejected changes"))
        self.dialog.confirm.accepted.connect(self.commit_changes)
        self.dialog.show()

    def updateResults(self):
        print("changes were made!")
        self.updateTab.emit()

    @pyqtSlot()
    def commit_changes(self):
        self.commitWorker=commitData(self.auth,self.model.item)
        self.commitWorker.signals.finished.connect(self.updateResults)
        self.commitWorker.signals.hasError.connect(lambda x:QErrorMessage(self.parent).showMessage(str(x)))
        self.commitWorker.signals.hasResponse.connect(lambda x:print(x))

        QThreadPool.globalInstance().start(self.commitWorker)
