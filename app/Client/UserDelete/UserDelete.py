from PyQt5.QtCore import QRunnable,QObject,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QDialog,QTableView
from ..MainWindow.default_fields import *
from ..MainWindow.ModelDelegates import *
from ..MainWindow.TableModel import *
from .workers.DeleteUser import DeleteUser

class UserDelete:
    def __init__(self,auth,parent,widget,name):
        self.auth=auth
        self.parent=parent
        self.name=name
        self.widget=widget
        self.model=TableModel(item=user(),ReadOnly=TableModelEnum.READONLY)
        widget.view.setModel(self.model)
        prep_table(widget.view)
        widget.clear.clicked.connect(self.clear_view)
        widget.delete_btn.clicked.connect(self.delete_user)

    def clear_view(self,state):
        self.model.load_data(user(),re=True)

    def delete_user(self,state):
        print(self.model.item.get("id"))
        self.Deleter=DeleteUser(self.auth,self.model.item.get("id"))
        self.Deleter.signals.finished.connect(lambda:print("done deleting user"))
        self.Deleter.signals.hasError.connect(lambda x:print(x,"error"))
        self.Deleter.signals.hasResponse.connect(lambda x:print(x,"response"))
        QThreadPool.globalInstance().start(self.Deleter)
        self.clear_view(True)

    def setDelegates(self):
        self.widget.view.reset()
        self.widget.view.setModel(self.model)
        #if 'roles' in self.model.item.keys():
        #    self.model.item.__delitem__("roles")
        for num,k in enumerate(self.model.item.keys()):
            #print(k,"update user",num)
            if k == 'active':
                self.widget.view.setItemDelegateForRow(num,CheckBoxDelegate(self.widget,state=self.model.item.get(k)))
            elif k == 'password':
                self.widget.view.setItemDelegateForRow(num,TextEditDelegate(self.widget,password=True))
            elif k == 'phone':
                self.widget.view.setItemDelegateForRow(num,PhoneTextEditDelegate(self.widget))
            elif k == 'role':
                self.widget.view.setItemDelegateForRow(num,ComboBoxDelegate(self.widget,values=['admin','user']))
            else:
                self.widget.view.setItemDelegateForRow(num,TextEditDelegate(self.widget))


