class MenuBar:
    def __init__(self,parent):
        self.parent=parent
        parent.actionLogout.triggered.connect(self.invalidus)
        parent.actionExit.triggered.connect(parent.close)
    def invalidus(self):
        loggin=self.parent.loggin
        index=self.parent.stackedWidget.indexOf(loggin)
        self.parent.stackedWidget.setCurrentIndex(index)
        self.parent.auth=dict()
        self.parent.username.setText("")
        self.parent.password.setText("")
