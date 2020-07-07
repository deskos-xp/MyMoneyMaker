from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
import os,sys,json

from ..MainWindow.default_fields import *
from ..MainWindow.TableModel import TableModel,TableModelEnum
from ..MainWindow.ModelDelegates import *
from .workers.RefreshUser import RefreshUser

class UserReview(QWidget):
    def __init__(self,auth,parent,widget,name):
        self.parent=parent
        self.auth=auth
        self.widget=widget
        self.name=name
        self.model=TableModel(item=user(),ReadOnly=TableModelEnum.READONLY)
        super(QWidget,self).__init__()
        widget.view.setModel(self.model)
        prep_table(widget.view)

        widget.refresh.clicked.connect(self.requestRefresh)

    def requestRefresh(self,state):
        self.refreshUser=RefreshUser(self.auth,self.model.item.get("id"))
        self.refreshUser.signals.finished.connect(lambda:print("finished refreshing user"))
        self.refreshUser.signals.hasError.connect(lambda x:print(x,"error"))
        self.refreshUser.signals.hasResponse.connect(lambda x:print(x,'response'))
        self.refreshUser.signals.hasUser.connect(self.updateUser)
        QThreadPool.globalInstance().start(self.refreshUser)

    def updateUser(self,user):
        self.model.load_data(user,re=True)
