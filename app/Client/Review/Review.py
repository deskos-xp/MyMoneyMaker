from PyQt5 import uic
from PyQt5.QtCore import QObject,QRunnable,QThread,QThreadPool,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QWidget,QPushButton,QLCDNumber
import os,sys,json,requests
from .workers.ReviewLast import ReviewLast
from ..MainWindow.TableModel import TableModel,TableModelEnum
from ..MainWindow.default_fields import *
from copy import deepcopy

class Review(QWidget):
    def __init__(self,auth:dict,parent):
        self.parent=parent
        
        self.auth=parent.user
        print(self.auth,"auth "*10)
        super(Review,self).__init__()
        
        uic.loadUi("Client/MainWindow/forms/review.ui",parent.review)
        self.parent.review.refresh.clicked.connect(self.builderReview)
        self.model=TableModel(item=currency(),ReadOnly=TableModelEnum.READONLY)
        self.parent.review.view.setModel(self.model)
        prep_table(self.parent.review.view)
        self.updateTotalLCD()
        self.parent.tabWidget.currentChanged.connect(parent.review.refresh.click)

    def updateTotalLCD(self):
        self.model.layoutChanged.connect(self.handleChanges)

    def handleChanges(self):
        total=0
        for k in currency():
            if k not in ["id","date"]:
                if self.model.item.get(k) != None:
                    if k in ['pennies','nickels','dimes','quarters']:
                        if k == 'pennies':
                            total+=self.model.item.get(k)*0.01
                        elif k == "nickels":
                            total+=self.model.item.get(k)*0.05
                        elif k == "dimes":
                            total+=self.model.item.get(k)*0.1
                        elif k == "quarters":
                            total+=self.model.item.get(k)*0.25
                    else:
                        if k == "dollar":
                            total+=self.model.item.get(k)
                        elif k == "dollar5":
                            total+=(self.model.item.get(k)*5)
                        elif k == "dollar10":
                            total+=(self.model.item.get(k)*10)
                        elif k == "dollar20":
                            total+=(self.model.item.get(k)*20)
                        elif k == "dollar50":
                            total+=(self.model.item.get(k)*50)
                        elif k == "dollar100":                        
                            total+=(self.model.item.get(k)*100)
        self.parent.review.total.display(total)
    
    def hasData(self,data):
        d=data.get("status")
        self.model.load_data(data.get(d),re=True)

    def builderReview(self):
        print(self.auth)
        self.reviewLast=ReviewLast(self.auth)
        self.reviewLast.signals.finished.connect(lambda: print("finished getting review from server"))
        self.reviewLast.signals.hasResponse.connect(lambda x:print(x))
        self.reviewLast.signals.hasError.connect(lambda x:print(x))
        self.reviewLast.signals.hasData.connect(self.hasData)
        QThreadPool.globalInstance().start(self.reviewLast)
        
