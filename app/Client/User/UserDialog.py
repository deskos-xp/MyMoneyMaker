from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QWidget
import os,sys,json
from pathlib import Path
from ..UserDelete.UserDelete import UserDelete
from ..UserNew.UserNew import UserNew
from ..UserSearch.UserSearch import UserSearch
from ..UserUpdate.UserUpdate import UserUpdate
inst=[UserUpdate,UserNew,UserSearch,UserDelete]
import enum
class inst(enum.Enum):
    update_user_widget=UserUpdate
    new_user_widget=UserNew
    search_user_widget=UserSearch
    delete_user_widget=UserDelete


class UserDialog(QDialog):
    def __init__(self,parent):
        self.parent=parent
        self.auth=parent.stacks['charting'].auth
        super(UserDialog,self).__init__()

        self.dialog=QDialog(parent)
        self.names=list()
        self.views=dict()
        self.widgets=dict()
        try:
            uic.loadUi("Client/MainWindow/forms/userdialog.ui",self.dialog)
            self.before_loadUis()
            self.loadUis()
        except Exception as e:
            print(e)
        
        #print(self.auth)
        self.dialog.show()

    def prep_ui(self,name):
        self.widgets[name]=getattr(self.dialog,name)
        try:
            uic.loadUi("Client/MainWindow/forms/{ii}.ui".format(**dict(ii=name)),self.widgets[name])
            #self.views[w[num]]=inst[num](self.auth,self,x,w[num])
            self.views[name]=inst.__dict__.get(name).value(self.auth,self,self.widgets[name],name)
        except Exception as e:
            print(e,"error "*10)

    def before_loadUis(self):
        w=['update','new','search','delete']
        for num,i in enumerate(w):
            if i != 'search':
                continue
            self.names.append("{}_user_widget".format(i))

    def loadUis(self):
        for i in self.names:
            self.prep_ui(i)
