from ..models.User import User
from .. import db,auth,app

def verify_password(username,password):
    user=db.session.query(User).filter(User.uname.in_([username])).first()
    if not user or not user.verify_password(password):
        return dict(user=None,authorized=False)
    if not user.active:
        return dict(user=None,authorized=False)
    return dict(user=user,authorized=True)
