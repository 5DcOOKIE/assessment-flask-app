from flask_httpauth import HTTPBasicAuth
from .db import User, db

auth = HTTPBasicAuth()


@auth.verify_password
def authenticate(email, password):
    q = db.session.query(User).filter(
        User.email == email, User.password == password)
    if q.count() == 1:
        return True
    return False
