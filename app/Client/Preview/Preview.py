from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QDialog
from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import TableModel,TableModelEnum
from copy import deepcopy
class Preview(QDialog):
    def __init__(self,parent,data):
        self.parent=parent
        super(Preview,self).__init__()
        self.gui=QDialog(parent)
        uic.loadUi("Client/MainWindow/forms/preview.ui",self.gui)
       
        data=deepcopy(data)
        data.__delitem__('id')
 
        self.model=TableModel(item=data,ReadOnly=TableModelEnum.READONLY)
        self.gui.view.setModel(self.model)
        
        total=0
        for k in currency_mx().keys():
            total+=data.get(k)*currency_mx().get(k)
        self.gui.total.display(total)

        self.gui.show()        
