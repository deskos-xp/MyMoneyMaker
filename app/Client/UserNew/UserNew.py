from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json
from ..MainWindow.default_fields import *
from ..MainWindow.ModelDelegates import *
from ..MainWindow.TableModel import *
from copy import deepcopy
from PyQt5.QtGui import QIcon
from .workers.SaverUser import SaveUser

class UserNew:
    def __init__(self,auth,parent,widget,name):
        self.auth=auth
        self.parent=parent
        self.widget=widget
        self.name=name

        self.user=user()
        self.user.__delitem__("")
        self.model=TableModel(item=deepcopy(self.user),ReadOnly=TableModelEnum.READONLY_FIELDS,ReadOnlyFields=['id'])
        widget.editor.setModel(self.model)
        prep_table(widget.editor)
        self.setDelegates()
        
        widget.clear.setIcon(QIcon.fromTheme("delete_table"))
        widget.clear.clicked.connect(self.resetTable)

        widget.save.setIcon(QIcon.fromTheme("document-save"))
        widget.save.clicked.connect(self.save)

    def save(self,state):
        print(self.model.item)
        self.saveUser=SaveUser(self.auth,self.model.item)
        self.saveUser.signals.finished.connect(lambda :print("user finished saving"))
        self.saveUser.signals.hasError.connect(lambda x:print(x,"error"))
        self.saveUser.signals.hasResponse.connect(lambda x:print(x))
        QThreadPool.globalInstance().start(self.saveUser)

    def resetTable(self,state):
        self.model.load_data(deepcopy(self.user),re=True)
        self.setDelegates()

    def setDelegates(self):
        self.widget.editor.reset()
        self.widget.editor.setModel(self.model)
        #if 'roles' in self.model.item.keys():
        #    self.model.item.__delitem__("roles")
        for num,k in enumerate(self.model.item.keys()):
            print(k,"update user",num)
            if k == 'active':
                self.widget.editor.setItemDelegateForRow(num,CheckBoxDelegate(self.widget,state=self.model.item.get(k)))
            elif k == 'password':
                self.widget.editor.setItemDelegateForRow(num,TextEditDelegate(self.widget,password=True))
            elif k == 'phone':
                self.widget.editor.setItemDelegateForRow(num,PhoneTextEditDelegate(self.widget))
            elif k == 'role':
                self.widget.editor.setItemDelegateForRow(num,ComboBoxDelegate(self.widget,values=['admin','user']))
            else:
                self.widget.editor.setItemDelegateForRow(num,TextEditDelegate(self.widget))


