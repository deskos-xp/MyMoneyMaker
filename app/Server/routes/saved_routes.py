from flask import make_response,request,session
from flask import current_app as app
from ..models.Saved import db,auth,ma,Saved,SavedSchema
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from .decor import roles_required
from ..messages import messages

@app.route("/saved/delete/<ID>",methods=['delete'])
@auth.login_required
@roles_required(roles=['admin'])
def delete_saved(ID):
    if not ID:
        return messages.NO_ID.value
    else:
        return delete(ID,Saved)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/saved/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_saved_id(ID):
    user_id=session.get('user_id').get('id')
    if ID == None:
        return status(Saved(),status=status_codes.NO_ID_PROVIDED,msg="no saved id provided!")
    saved=db.session.query(Saved).filter_by(**dict(id=ID,user_id=user_id)).first()
    if Saved == None:
        return status(Saved(),status=status_codes.INVALID_ID,msg="invalid saved!")
    savedSchema=SavedSchema()
    return status(Saved(),status=status_codes.OBJECT,object=savedSchema.dump(saved))

@app.route("/saved/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_saved():
    user_id=session.get('user_id').get('id')
    json=request.get_json(force=True)
    json=ccj(json)
    #print(json)
    #assert json != None
    if not json:
        if json != {}:
            return messages.NO_JSON.value
    page=json.get('page')
    limit=json.get('limit')
    if page == None:
        page=0
    if limit == None:
        limit=10

    if json.get('limit') != None:
        json.__delitem__('limit')
    if json.get('page') != None:
        json.__delitem__('page')
    json['user_id']=user_id

    savedes=db.session.query(Saved).filter_by(**json).limit(limit).offset(page*limit).all()
    savedSchema=SavedSchema()
    savedes=[savedSchema.dump(i) for i in savedes]
    return status(Saved(),status=status_codes.OBJECTS,objects=Json.dumps(savedes))

@app.route("/saved/get/last",methods=["get"])
@auth.login_required
@roles_required(roles=["admin","user"])
def get_last():
    user_id=session['user_id']
    user_id=user_id.get("id")
    print(user_id)
    last=db.session.query(Saved).filter_by(**dict(user_id=user_id)).all()

    #last=db.session.query(Saved).filter_by(**dict(user_id=user_id)).all()
    if last and len(last) > 0:
        return status(Saved(),status=status_codes.OBJECT,object=SavedSchema().dump(last[-1]))
    else:
        return status(Saved(),status="nothing to see!")

@app.route("/saved/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def add_saved():
    json=request.get_json(force=True)
    json=ccj(json)
    if not json:
        return messages.NO_JSON.value
    '''
    if len(json.keys()) > 0:
        saved=db.session.query(Saved).filter_by(**json).first()
        if saved != None:
            return  status(saved,status=status_codes.OLD)
    '''
    user_id=session.get('user_id').get('id')
    json['user_id']=user_id
    saved=Saved(**json)
    db.session.add(saved)
    db.session.commit()
    db.session.flush()
    return status(saved,status=status_codes.NEW)


@app.route("/saved/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_saved(ID):
    print(ID,"update id")
    user_id=session.get("user_id").get("id")
    if not ID:
        return messages.NO_ID.value
    saved_old=db.session.query(Saved).filter_by(**dict(id=ID,user_id=user_id)).first()
    if not saved_old:
        return messages.ENTITY_DOES_NOT_EXIST.value
    json=request.get_json(force=True)
    json=ccj(json)
    if not json:
        return messages.NO_JSON.value
    for key in saved_old.defaultdict().keys():
        if key not in ["id"]:
            #assert key in saved_old.__dict__.keys()
            if key not in saved_old.__dict__.keys():
                return messages.INVALID_KEY_ADDRESS.value

            #assert key in json.keys()
            if key not in json.keys():
                return messages.INVALID_KEY_ADDRESS.values

            saved_old.__dict__[key]=json[key]
            flag_modified(saved_old,key)
    db.session.merge(saved_old)
    db.session.flush()
    db.session.commit()
    return status(saved_old,status=status_codes.UPDATED)

