from PyQt5.QtCore import Qt,pyqtSlot,QDate
from PyQt5.QtWidgets import QHeaderView,QItemDelegate,QComboBox,QCheckBox,QDateEdit,QTextEdit,QLineEdit,QSpinBox,QPushButton,QStyledItemDelegate,QStyleOptionViewItem
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPalette
import time
import phonenumbers
import sys
class PhoneTextEditDelegate(QItemDelegate):
    def __init__(self,parent):
        QItemDelegate.__init__(self,parent)
        self.formatted=""

    def createEditor(self,parent,option,index):
        date=QLineEdit(parent) 
        def formatter():
            try:
                self.formatted=phonenumbers.format_number(phonenumbers.parse(self.sender().text(),"US"),phonenumbers.PhoneNumberFormat.NATIONAL)
                #print(self.formatted)
            except Exception as e:
                print(e)
        date.textChanged.connect(formatter)
        date.setText(index.model().data(index))
        return date

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index)) 
        editor.setText(self.formatted)
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,self.formatted,Qt.EditRole)
    
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
 
class ButtonDelegate(QItemDelegate):
    def __init__(self,parent,action):
        QItemDelegate.__init__(self,parent)
        self.action=action

    def createEditor(self,parent,option,index):
        date=QPushButton(parent)
        def act(state):
            acted=self.action()
            if acted:
                index.model().setData(index,acted,Qt.EditRole)
            
        date.clicked.connect(act)

        return date

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        #editor.setText(index.model().data(index)) 
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.text(),Qt.EditRole)
    
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
 
class SpinBoxDelegate(QItemDelegate):
    def __init__(self,parent):
        QItemDelegate.__init__(self,parent)
        
    def createEditor(self,parent,option,index):
        date=QSpinBox(parent)
        date.setMaximum(2147483647)
        date.setMinimum(-2147483647)

        return date

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        if index.model().data(index) == None:
            editor.setValue(0)
        else:            
            editor.setValue(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.value(),Qt.EditRole)
    
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
 
class TextEditDelegate(QStyledItemDelegate):
    def __init__(self,parent,password=False):
        QStyledItemDelegate.__init__(self,parent)
        self.password=password
        def paint(painter, option, index):
            #print("painted! "+time.ctime())
            QStyledItemDelegate.paint(self, painter, option, index)
            
            painter.save()
            try:
                if index.column() <1:
                    alignment=Qt.AlignLeft
                else:
                    alignment=Qt.AlignCenter
                r=QRect(option.rect)
                painter.fillRect(option.rect,option.palette.color(QPalette.Active,QPalette.Light))
                if index.column() > 0:
                    painter.drawText(option.rect,alignment,'*'*len(index.model().data(index)))
                else:
                    painter.drawText(option.rect,alignment,index.model().data(index))

                #self.do_paint(painter, option, index)
            except Exception as e:
                print(e)
            painter.restore()


        if password:
            self.paint=paint

    def createEditor(self,parent,option,index):
        t=index.model().data(index)
        if isinstance(t,list):
            t=t[0]
        if isinstance(t,dict):
            t=t.get("name")

        if self.password == False:
            date=QTextEdit(parent)
        else:
            date=QLineEdit(parent)
            date.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        date.setText(t)                
        return date

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        t=index.model().data(index)
        if isinstance(t,list):
            t=t[0]
        if isinstance(t,dict):
            t=t.get("name")
        editor.setText(t)        
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        '''
        t=index.model().data(index)
        if isinstance(t,list):
            t=t[0]
        if isinstance(t,dict):
            t=t.get("name")
        '''
        if self.password == False:
            model.setData(index,editor.toPlainText(),Qt.EditRole)
        else:
            model.setData(index,editor.text(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
 

class DateEditDelegate(QItemDelegate):
    def __init__(self,parent):
        QItemDelegate.__init__(self,parent)

    def createEditor(self,parent,option,index):
        date=QDateEdit(parent)
        date.setCalendarPopup(True)
        return date

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        d=index.model().data(index)
        if d != '':
            asTime=time.strptime(d,"%m/%d/%Y")
            asTuple=(asTime.tm_year,asTime.tm_mon,asTime.tm_mday)
            editor.setDate(QDate(*asTuple))
        #print(d)
        
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        #model.setData(index,editor.
        #print(type(editor.date().getDate()))
        d="{1}/{2}/{0}".format(*editor.date().getDate())
        model.setData(index,d,Qt.EditRole)
        #print(editor.date())
    
    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
    
class ComboBoxDelegate(QItemDelegate):
    def __init__(self,parent,values=[]):
        QItemDelegate.__init__(self,parent)
        self.values=values

    def createEditor(self,parent,option,index):
        box=QComboBox(parent)
        box.addItems(self.values)
        return box

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        editor.setCurrentText(index.model().data(index))
        editor.blockSignals(False)
    def setModelData(self,editor,model,index):
        model.setData(index,editor.currentText(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
       self.commitData.emit(self.sender())


class CheckBoxDelegate(QItemDelegate):
    def __init__(self,parent,state=False):
        QItemDelegate.__init__(self,parent)
        self.state=state

    def createEditor(self,parent,option,index):
        box=QCheckBox(parent)
        box.setChecked(self.state)
        return box

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        editor.setChecked(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self,editor,model,index):
        model.setData(index,editor.isChecked(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender()) 
    
class LineEditDelegate(QItemDelegate):
    def __init__(self,parent):
        QItemDelegate.__init__(self,parent)

    def createEditor(self,parent,option,index):
        box=QLineEdit(parent)
        box.setText(index.model().data(index))
        return box

    def setEditorData(self,editor,index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)
    def setModelData(self,editor,model,index):
        model.setData(index,editor.text(),Qt.EditRole)

    @pyqtSlot()
    def currentIndexChanged(self):
       self.commitData.emit(self.sender())

