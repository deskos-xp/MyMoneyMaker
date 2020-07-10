from flask import request,make_response
from flask import current_app as app
from ..models.User import User,db,UserSchema,auth
from ..config.Config import Config
from . import verify
from .decor import roles_required
import os,sys
import json as Json
from .. import status,delete,ccj,status_codes
from ..messages import messages
from sqlalchemy.orm.attributes import flag_modified

@app.route("/user/delete/<user_id>",methods=["delete"])
@auth.login_required
@roles_required(roles=["admin"])
def delete_user(user_id):
    if not user_id:
        return "no user id provided",401
    print(user_id,"server user id")
    USER=db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()
    return "delete user pending"

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/user/get/<ID>",methods=['get'])
@auth.login_required
@roles_required(roles=['admin','user'])
def getUserId(ID):
    if not ID:
        return "no id provided",402
    USER=db.session.query(User).filter_by(id=ID).first()
    if not USER:
        return "no user",402
    USER.password="x"*8
    userSchema=UserSchema()

    return status(User(),status="object",object=userSchema.dump(USER))

@app.route("/user/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def search_user():
    print(request.view_args)
    json=request.get_json(force=True)
    if not json:
        return messages.NO_JSON.value
    json=ccj(json)
    page=json.get("page")
    limit=json.get("limit")
    if page != None:
        json.__delitem__("page")
    if limit != None:
        json.__delitem__("limit")

    if page == None:
        page=0
    if limit == None:
        limit=10
    userSchema = UserSchema()
    USERS=db.session.query(User).filter_by(**json).limit(limit).offset(limit*page).all()
    users_j=[userSchema.dump(i) for i in USERS]
    #do not transmit password hashes
    for u in users_j:
        u['password']="xxxxx"
    return status(User(),status=status_codes.OBJECTS,objects=Json.dumps(users_j))

@app.route("/user/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def alter_user(ID):
    json=request.get_json(force=True)
    json=ccj(json)
    #assert ID == request.view_args['ID']
    #print(ID)
    #getuser
    admin=db.session.query(User).filter_by(uname=auth.username()).first()
    #assert admin != None
    if not admin:
        return messages.ENTITY_DOES_NOT_EXIST_USER.value
    USER=db.session.query(User).filter_by(id=ID).first()
    #assert USER != None
    print(ID)
    if not USER:
        return messages.ENTITY_DOES_NOT_EXIST_USER.value
    '''
    if 'role' in json.keys():
        json.__delitem__('role')
    if 'roles' in json.keys():
        json.__delitem__('roles')
    '''
    j=jsonToDict(json)
    for k in j.keys():
        #if k not in ['roles','role']:
            USER.__dict__[k]=j.get(k)
            flag_modified(USER,k)
        #else:
        #    USER.__dict__['roles'].clear()
        #    USER.__dict__['roles'].append(j.get(k))
        #    flag_modified(USER,'roles')
    #USER.lname=json.get("lname")
    db.session.merge(USER)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)


def jsonToDict(json) -> dict:
    d=dict()
    for key in json.keys():
        d[key]=json.get(key)
    return d


if Config().NEED_ADMIN == True:
    #if os.environ['NEED_ADMIN'] == "True":
    @app.route("/admin/new",methods=["get"])
    def new_admin():
        #if os.environ['NEED_ADMIN'] == "True":
        result=default_user()
        if result[1] == 200:
            return status(User(),status=status_codes.NEW,msg="admin created! please set need_admin to false and restart server!")
        else:
            return status(User(),status=status_codes.OLD,msg=result[0])
@app.route("/user/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def new_user():
    json=request.get_json(force=True)
    if not json:
        return messages.NO_JSON.value
    json=ccj(json)
    print(json)
    if db.session.query(User).filter_by(uname=auth.username()).first().active:
        print(json)
        user=User(**json)

        user.hash_password(json['password'])
        json.__delitem__('password')
        exists=db.session.query(User).filter_by(**json).first()
        print(exists)
        if exists != None:
            return status(exists,status=status_codes.OLD)
        
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        return status(db.session.query(User).filter_by(uname=json['uname']).first(),status=status_codes.NEW)
        #return status(user,"new")
    else:
        return status(User(),status=status_codes.INVALID_ID)

def query_user(uname="admin"):
    user = session.query(User).filter_by(uname="admin").first()
    print(user)
    return user;

def default_user():
    default_user = User(uname="admin",fname="first_name",mname="middle_name",lname="last_name",email="admin@localhost",phone="5"*11,active=True,role='admin')
    user=db.session.query(User).filter_by(uname=default_user.uname).first()
    if user:
        return "user exists",400
    default_user.hash_password("avalon")
    db.session.add(default_user)
    db.session.commit()
    return "user created",200
