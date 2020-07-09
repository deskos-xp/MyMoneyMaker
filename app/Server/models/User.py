from .. import db,auth,ma
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__="users"
    def hash_password_auto(self):
        self.password=pwd_context.encrypt(self.password)
    def hash_password(self,password):
        self.password=pwd_context.encrypt(password)
    def verify_password(self,password):
        i=pwd_context.verify(password,self.password)
        return i
    id=db.Column(db.Integer(),primary_key=True)
    role=db.Column(db.String(length=128))
    uname=db.Column(db.String(length=50))
    fname=db.Column(db.String(length=50))
    lname=db.Column(db.String(length=50))
    mname=db.Column(db.String(length=50))
    email=db.Column(db.String(length=128))
    phone=db.Column(db.String(length=15))
    active=db.Column(db.Boolean)
    password=db.Column(db.String(length=128))

    def __repr__(self):
        return '''
        User(
            id={id},
            roles={roles},
            uname={uname},
            fname={fname},
            mname={mname},
            lname={lname},
            email={email},
            phone={phone},
            active={active},
            password={password}
        '''.format(dict(
            id=self.id,
            role=self.role,
            uname=self.uname,
            fname=self.fname,
            mname=self.mname,
            lname=self.lname,
            email=self.email,
            active=self.active,
            password=self.password  
        ))
    def defaultdict(self):
        return dict(
            id=self.id,
            role=self.role,
            uname=self.uname,
            fname=self.fname,
            mname=self.mname,
            lname=self.lname,
            email=self.email,
            active=self.active,
            password=self.password  
        )

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model=User
        fields=("id","uname","fname","mname","lname","email","phone","active","role")
    id=ma.auto_field()
    role=ma.auto_field()
    uname=ma.auto_field()
    fname=ma.auto_field()
    mname=ma.auto_field()
    lname=ma.auto_field()
    email=ma.auto_field()
    phone=ma.auto_field()
    active=ma.auto_field()
    password=ma.auto_field()

