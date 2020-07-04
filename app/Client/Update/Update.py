from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import os,sys,json,requests
from ..MainWindow.TableModel import TableModel,TableModelEnum
from ..MainWindow.default_fields import *
from ..MainWindow.ListModel import ListModel
from ..MainWindow.ModelDelegates import *
from copy import deepcopy
from .workers.getSavedEntries import getSavedEntries
from ..UpdateDialog.UpdateDialog import UpdateDialog

class Update(QWidget):
    def __init__(self,parent):
        self.parent=parent
        self.auth=dict()
        super(Update,self).__init__()
        uic.loadUi("Client/MainWindow/forms/update_search.ui",parent.update)

        self.model=TableModel(item=currency_ut_plus())
        parent.update.searchView.setModel(self.model)
        prep_table(parent.update.searchView)

        self.resultsModel=ListModel()
        parent.update.resultsView.setModel(self.resultsModel)
        
        parent.update.search.clicked.connect(self.search)
        parent.update.search.setIcon(QIcon.fromTheme("search.svg"))
        
        parent.update.clear.clicked.connect(self.clear)
        parent.update.clear.setIcon(QIcon.fromTheme("delete_table.svg"))
        parent.update.resultsView.activated.connect(self.showResult)
        self.prepDelegates(parent)


    def showResult(self,index):
        displayed_text=index.model().data(index,Qt.DisplayRole)
        row=index.row()
        #print(self.resultsModel.items[row])
        self.updateDialog=UpdateDialog(self.auth,self.resultsModel.items[row])
        self.updateDialog.updateTab.connect(self.parent.update.search.click)

    def prepDelegates(self,parent):
        for num,key in enumerate(self.model.item.keys()):
            #print(key)
            if key in currency_mx().keys() or key in ['page','limit']:
                parent.update.searchView.setItemDelegateForRow(num,SpinBoxDelegate(parent.update.searchView))
            elif key == 'date':
                parent.update.searchView.setItemDelegateForRow(num,DateEditDelegate(parent.update.searchView))

    def clear(self):
        self.resultsModel.items.clear()
        self.resultsModel.layoutChanged.emit()
        self.model.load_data(currency_ut_plus(),re=True)
        self.prepDelegates(self.parent)        

    def store_data(self,data):
        self.resultsModel.items.clear()
        for u in data:
            self.resultsModel.items.append(u)
        self.resultsModel.layoutChanged.emit()

    def search_Worker(self,search_data):
        self.searchWorker=getSavedEntries(self.auth,search_data)
        self.searchWorker.signals.finished.connect(lambda :print("finished getting data"))
        self.searchWorker.signals.hasError.connect(lambda x:print(x,"error"))
        self.searchWorker.signals.hasResponse.connect(lambda x:print(x))
        self.searchWorker.signals.hasData.connect(self.store_data)
        QThreadPool.globalInstance().start(self.searchWorker)
    
    def search(self):
        searchable=deepcopy(self.model.item)
        rem=[]
        for k in searchable.keys():
            if searchable[k] == currency_ut_plus()[k]:
                rem.append(k)
        for k in rem:
            searchable.__delitem__(k)
        #print(searchable,'searchable'*10)
        self.search_Worker(searchable)
