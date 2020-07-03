from email_validator import validate_email

class emailLS:
    def __init__(self,email,dest="email_is_what",debug=False):
        self.__dict__[dest]=None
        self.email=email
        try:
            self.__dict__[dest]=validate_email(email)
        except Exception as e:
            self.__dict__[dest]=False
            if debug == True:
                print(e)
             
