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
from .workers.SearchUser import SearchUser

class UserSearch(QWidget):
    def __init__(self,auth,parent,widget,name):
        super(UserSearch,self).__init__()
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

        widget.search.clicked.connect(self.searchF) 
        widget.clear.clicked.connect(self.clear)

        self.model_list=ListModel(custom="{id} - {uname}")
        widget.results.setModel(self.model_list)
        widget.results.activated.connect(self.activatedSelection)

    def activatedSelection(self,select):
        print(select.model().data(select,Qt.DisplayRole))
        print(self.model_list.items[select.row()])

    @pyqtSlot(bool)
    def searchF(self,state):
        @pyqtSlot(list)
        def Users(users):
            print(users)
            self.model_list.items.clear()
            for u in users:
                self.model_list.items.append(u)
            self.model_list.layoutChanged.emit()
                
        f=dict()
        
        for k in self.model_table.item.keys():
            if self.model_table.item.get(k) != user().get(k):
                f[k]=self.model_table.item.get(k)
        searchUsers=SearchUser(self.auth,f)
        searchUsers.signals.finished.connect(lambda : print("finished searchUser"))
        searchUsers.signals.hasError.connect(lambda x:print(x,"error"))
        searchUsers.signals.hasResponse.connect(lambda x:print(x,"response"))
        searchUsers.signals.hasUsers.connect(Users)
        QThreadPool.globalInstance().start(searchUsers)
        print(self.model_table.item,"search btn clicked",sep="\n")



    def clear(self):
        self.model_table.load_data(deepcopy(self.u),re=True)
        self.model_list.items.clear()
        self.model_list.layoutChanged.emit()
