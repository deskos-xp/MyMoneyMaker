from PyQt5 import uic
from PyQt5.QtCore import QRunnable,QObject,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog
from ..MainWindow.default_fields import *
from ..MainWindow.ListModel import ListModel
from ..MainWindow.TableModel import *
from ..MainWindow.ModelDelegates import *
import os,sys,json,requests
from pathlib import Path
from copy import deepcopy

class UserSearch:
    def __init__(self,auth,parent,widget,name):
        self.auth=auth
        self.parent=parent
        self.name=name
        self.widget=widget
        print(name)
        
        self.u= {i:user()[i] for i in user().keys() if i != ""}       

        self.model_table=TableModel(item=deepcopy(self.u))
        widget.editor.setModel(self.model_table)
        prep_table(widget.editor)

        for num,key in enumerate(self.model_table.item.keys()):
            if key.lower() == 'active':
                widget.editor.setItemDelegateForRow(num,CheckBoxDelegate(widget))
            elif key.lower() == "email":
                widget.editor.setItemDelegateForRow(num,TextEditDelegate(widget))
            elif key.lower() == "password":
                widget.editor.setItemDelegateForRow(num,TextEditDelegate(widget,password=True))
            elif key.lower() == "id":
                widget.editor.setItemDelegateForRow(num,SpinBoxDelegate(widget))
            else:
                widget.editor.setItemDelegateForRow(num,LineEditDelegate(widget))

        widget.search.clicked.connect(self.search) 
        widget.clear.clicked.connect(self.clear)

        self.model_list=ListModel()
        widget.results.setModel(self.model_list)

    def search(self):
        print(self.model_table.item,"search btn clicked",sep="\n")

    def clear(self):
        self.model_table.load_data(deepcopy(self.u),re=True)
        self.model_list.items.clear()
        self.model_list.layoutChanged.emit()
