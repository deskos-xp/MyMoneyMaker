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

class UserDialog(QDialog):
    def __init__(self,parent):
        self.parent=parent
        self.auth=parent.stacks['charting'].auth
        super(UserDialog,self).__init__()

        self.dialog=QDialog(parent)
        self.views=dict()
        try:
            uic.loadUi("Client/MainWindow/forms/userdialog.ui",self.dialog)
            self.loadUis()
        except:
            pass
        
        #print(self.auth)
        self.dialog.show()

    def loadUis(self):
        w=['update','new','search','delete']
        for num,i in enumerate(w):
            print(num)
            w[num]="{}_user_widget".format(i)
            x=getattr(self.dialog,w[num])
            try:
                uic.loadUi("Client/MainWindow/forms/{ii}.ui".format(**dict(ii=w[num])),x)
                self.views[w[num]]=inst[num](self.auth,self,x,w[num])
            except Exception as e:
                print(e)
