from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget

from ..MainWindow.default_fields import *
from ..MainWindow.ModelDelegates import *
from ..MainWindow.TableModel_editor import TableModel_editor as TableModel,TableModel_editorEnum as TableModelEnum

from ..Review.workers.ReviewLast import ReviewLast
from .workers.NewEntryWorker import NewEntryWorker

class NewEntry(QWidget):
    def __init__(self,parent):
        self.auth=dict()
        self.parent=parent
        super(NewEntry,self).__init__()
        uic.loadUi("Client/MainWindow/forms/new_entry.ui",parent.newEntry)

        self.model=TableModel(item=currency())

        parent.newEntry.editor.setModel(self.model)
        prep_table(parent.newEntry.editor)
        self.prep_delegates(parent.newEntry.editor)
        parent.tabWidget.currentChanged.connect(parent.newEntry.clear.click)
        self.buttons()

    def prep_delegates(self,table):
        for num,k in enumerate(self.model.item.keys()):
            if k == 'date':
                table.setItemDelegateForRow(num,DateEditDelegate(table))
            else:
                if k != 'id':
                    table.setItemDelegateForRow(num,SpinBoxDelegate(table)) 

    def builderWorker(self):
        self.workerReview=ReviewLast(self.auth)
        self.workerReview.signals.finished.connect(lambda : print("finished getting data"))
        self.workerReview.signals.hasResponse.connect(lambda x:print(x))
        self.workerReview.signals.hasData.connect(self.prep_data)
        self.workerReview.signals.hasError.connect(lambda x:print(x))
        QThreadPool.globalInstance().start(self.workerReview)


    def prep_data(self,data):
        d=data.get("status")
        if data.get(d).get("date") == "":
            data[d]['date']=time.strftime("%m/%d/%Y",time.localtime())
        self.model.load_data(data.get(d),re=True)
        self.prep_delegates(self.parent.newEntry.editor)
        
    def clearTable(self):
        #self.model.load_data(currency(),re=True)
        self.builderWorker()

    def commitTable(self):
        self.workerNew=NewEntryWorker(self.auth,self.model.item)
        self.workerNew.signals.hasError.connect(lambda x:print(x))
        self.workerNew.signals.hasResponse.connect(lambda x:print(x))
        self.workerNew.signals.finished.connect(self.parent.newEntry.clear.click)
        QThreadPool.globalInstance().start(self.workerNew)

    def buttons(self):
        self.parent.newEntry.clear.clicked.connect(self.clearTable)
        self.parent.newEntry.commit.clicked.connect(self.commitTable)
