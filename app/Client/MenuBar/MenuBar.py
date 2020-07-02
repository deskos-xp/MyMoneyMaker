from ..About.About import About
from ..ServerSettings.ServerSettings import ServerSettings
class MenuBar:
    def __init__(self,parent):
        self.parent=parent
        parent.actionLogout.triggered.connect(self.invalidus)
        parent.actionExit.triggered.connect(parent.close)
        parent.action_About.triggered.connect(self.about_)
        parent.action_Server_Settings.triggered.connect(self.serverSettings_)
        parent.stackedWidget.currentChanged.connect(self.lock_action_logout)
        self.lock_action_logout(0)


    def serverSettings_(self):
        dialog=ServerSettings("Server/config/env.json",self.parent)
        #dialog.show()

    def invalidus(self):
        loggin=self.parent.loggin
        index=self.parent.stackedWidget.indexOf(loggin)
        self.parent.stackedWidget.setCurrentIndex(index)
        self.parent.auth=dict()
        
        self.parent.stacks['login'].cachedUser()
        #self.parent.username.setText("")
        #self.parent.password.setText("")

    def lock_action_logout(self,index):
        print(self.parent.stackedWidget.currentIndex(),"logged in"*10)        
        ind=self.parent.stackedWidget.indexOf(self.parent.loggedIn)
        self.parent.actionLogout.setEnabled(self.parent.stackedWidget.currentIndex() == ind)

    def about_(self):
        a=About(self.parent)

