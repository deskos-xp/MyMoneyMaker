from PyQt5.QtCore import QAbstractListModel,Qt

class ListModel(QAbstractListModel):
    def __init__(self,*args,items=None,**kwargs):
        super(ListModel,self).__init__()
        self.items=items or []
        self.custom=None
        if kwargs.get("custom"):
            self.custom=kwargs.get("custom")

    def data(self,index,role):
        if role == Qt.DisplayRole:
            text=self.items[index.row()]
            if not self.custom:
                textTMP="{ID} - {DATE}".format(**dict(ID=text.get("id"),DATE=text.get("date")))
            else:
                textTMP=self.custom.format(**dict(self.items[index.row()]))
            return textTMP

    def rowCount(self,index):
        return len(self.items)

