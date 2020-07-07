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
from PyQt5.QtGui import QIcon

class UserSearch(QWidget):
    userSelected:pyqtSignal=pyqtSignal(dict)

    def __init__(self,auth,parent,widget,name):
        super(UserSearch,self).__init__()
        self.auth=auth
        self.parent=parent
        self.name=name
        self.widget=widget

        print(name)
        
        self.u= {i:user()[i] for i in user().keys() if i != ""}       
        self.u['page']=0
        self.u['limit']=15

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
            elif key.lower() in ["id","page","limit"]:
                widget.editor.setItemDelegateForRow(num,SpinBoxDelegate(widget))
            else:
                widget.editor.setItemDelegateForRow(num,LineEditDelegate(widget))

        widget.search.clicked.connect(self.searchF) 
        widget.search.setIcon(QIcon.fromTheme("search"))

        widget.clear.clicked.connect(self.clear)
        widget.clear.setIcon(QIcon.fromTheme("delete_table"))
        self.model_list=ListModel(custom="{id} - {uname}")
        widget.results.setModel(self.model_list)
        widget.results.activated.connect(self.activatedSelection)

    def activatedSelection(self,select):
        #user clicks on selection
            #a dialog appears prompting to update/delete/view user data
        #print(select.model().data(select,Qt.DisplayRole))
        selected=self.model_list.items[select.row()]
        self.userSelected.emit(selected)

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
            if self.model_table.item.get(k) != user().get(k) or k in ['page','limit']:
                f[k]=self.model_table.item.get(k)
        searchUsers=SearchUser(self.auth,f)
        print(f,"searchF "*10)
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
