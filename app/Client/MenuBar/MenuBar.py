from ..About.About import About
from ..ServerSettings.ServerSettings import ServerSettings
import getpass
from ..User.UserDialog import UserDialog
class MenuBar:
    def __init__(self,parent):
        self.parent=parent
        parent.actionLogout.triggered.connect(self.invalidus)
        parent.actionExit.triggered.connect(parent.close)
        parent.action_About.triggered.connect(self.about_)
        parent.action_Server_Settings.triggered.connect(self.serverSettings_)
        parent.stackedWidget.currentChanged.connect(self.lock_action_logout)
        self.lock_action_logout(0)

        parent.actionUser.triggered.connect(self.user_)

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
        state=self.parent.stackedWidget.currentIndex() == ind

        self.parent.actionLogout.setEnabled(state)
        self.parent.action_Server_Settings.setEnabled(state)
        self.parent.actionUser.setEnabled(state)

    def about_(self):
        a=About(self.parent)

    def user_(self):
        u=UserDialog(self.parent)
