from flask import Flask,Response,request,session,redirect,url_for
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.inspection import inspect
from . import models
import json,logging,os
from dotenv import load_dotenv
#from .config.config import Config
from .config.Config import Config
load_dotenv()
#from sql_alchemy_utils import auto_delete_orphans

#LOG=os.getenv(os.getenv("LOG"))
LOG=Config().LOG
if LOG:
    if os.path.exists(LOG) and os.path.isfile(LOG):
        os.remove(LOG)

logging.basicConfig(level=logging.INFO,filename=LOG,filemode="a")
db=SQLAlchemy()
ma=Marshmallow()
auth=HTTPBasicAuth()
class status_codes:
    DELETED="deleted"
    NEW="new"
    OLD="old"
    UPDATED="updated"
    NOT_UPDATED="not_updated"
    UPLOADED="uploaded"
    NOT_UPLOADED="not_uploaded"
    NO_ID_PROVIDED="no_id_provided"
    INVALID_ID="invalid_id"
    OBJECT="object"
    OBJECTS="objects"
    INVALID_EXPORT_FMT="invalid export format"
    EXPORTING="exporting data to {}"
    INVALID_EXPORT_OBJ_TYPE="invalid object type to export"
    INVALID_FMT_FOR_TO="invalid fmt to export to TO"
    REQURIED_JSON_NOT_PROVIDED="json required was not provided"
    NOT_DELETED="not_deleted"


def status(model_instance,status,msg=None,object=None,objects="[{}]"):
    keys=[i for i in status_codes.__dict__.keys() if not i.startswith("__") and not callable(getattr(status_codes,i)) and type(getattr(status_codes,i)) == type(str())]
    keys=[status_codes.__dict__[i] for i in keys]
    if status not in keys:
        raise AssertionError(status)
    return dict(
            type=model_instance.__class__.__name__,
            id=model_instance.id,
            status=status,
            msg=msg,
            object=object,
            objects=json.loads(objects)
            )
def pre_delete_dependents(model,ID):
    #delete relationships making use of model before deleting model
    obj=db.session.query(model).filter_by(id=ID).first()
    relations=inspect(obj.__class__).relationships.items()
    for name,related in relations:
        #db.session.query(bj.__class__).filter_by()
        #print(model.__class__.__name__)
        #print(name)
        #print(related)
        if model in getattr(obj,name):
            #auto_delete_orphans(related)
            getattr(obj,name).remove(model)
            db.session.flush()
            db.session.commit()
            print(model)

def pre_delete_dependencies(model):
    relations=[i for i in model.__mapper__.relationships]
    for i in relations:
        i=[]
    db.session.flush()
    db.session.commit()

def ccj(o):
    if type(o) == str:
        return json.loads(o)
    else:
        return o

def delete(ID,model):
    assert ID != None
    brand=db.session.query(model).filter_by(id=ID).first()
    if brand == None:
        print("3###")
        return status(model(),status=status_codes.NOT_DELETED,msg="{0} not deleted as {0} does not exist!".format(model.__name__))
    else:
        pre_delete_dependents(model,ID)
        print(brand.__class__.__name__,4)
        pre_delete_dependencies(brand)
        print(brand.__class__.__name__,3)
        db.session.delete(brand)
        print(brand.__class__.__name__,2)
        db.session.commit()
        print(brand.__class__.__name__)
        return status(model(),status=status_codes.DELETED,msg="{} has been deleted!".format(brand.__class__.__name__))


app=Flask(__name__,instance_relative_config=False)
def create_app():
    app.config.from_object(Config())
    #'config.Config')
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from .routes import user_routes,saved_routes
        #,counting_routes

        db.create_all()
    return app
