from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json,requests
from PyQt5.QtGui import QIcon

from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import *
from ..MainWindow.ModelDelegates import *
from ..UserReview.workers.RefreshUser import RefreshUser
from .workers.SaverUser import SaveUser

class UserUpdate(QWidget):
    def __init__(self,auth,parent,widget,name):
        self.auth=auth
        self.parent=parent
        self.widget=widget
        self.name=name
        super(UserUpdate,self).__init__()

        self.user=user()
        self.user.__delitem__("")
        
        self.model=TableModel(item=self.user,ReadOnly=TableModelEnum.READONLY_FIELDS,ReadOnlyFields=['id'])
        widget.editor.setModel(self.model)
        prep_table(widget.editor)
        for num,k in enumerate(self.model.item.keys()):
            print(k)
            if k == 'active':
                widget.editor.setItemDelegateForRow(num,CheckBoxDelegate(widget,state=self.model.item.get(k)))
            elif k == 'password':
                widget.editor.setItemDelegateForRow(num,TextEditDelegate(widget,password=True))
            elif k == 'phone':
                widget.editor.setItemDelegateForRow(num,PhoneTextEditDelegate(widget))
            else:
                widget.editor.setItemDelegateForRow(num,TextEditDelegate(widget))
        widget.clear.clicked.connect(self.refreshUser)
        widget.clear.setIcon(QIcon.fromTheme("delete_table"))

        widget.save.clicked.connect(self.updateUser)
        widget.save.setIcon(QIcon.fromTheme("document-save"))

    def updateUser(self,state):
        try:
            self.saver=SaveUser(self.auth,self.model.item)
            self.saver.signals.finished.connect(lambda :print("finished saving user updates"))
            self.saver.signals.hasError.connect(lambda x:print(x,"error"))
            self.saver.signals.hasResponse.connect(lambda x:print(x,'response'))
            QThreadPool.globalInstance().start(self.saver)
        except Exception as e:
            print(e)

        print(state)
    
    def refreshUser(self,state):
        print(state)
        self.refresher=RefreshUser(self.auth,self.model.item.get("id"))
        self.refresher.signals.finished.connect(lambda:print("finished refreshing user"))
        self.refresher.signals.hasError.connect(lambda x:print(x,"error"))
        self.refresher.signals.hasUser.connect(self.refreshUserData)
        QThreadPool.globalInstance().start(self.refresher)

    def refreshUserData(self,user):
        self.model.load_data(user,re=True)
