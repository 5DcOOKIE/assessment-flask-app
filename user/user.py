from flask import Blueprint, request
from flask import jsonify
from .db import User, db
from .auth import auth
from string import ascii_lowercase as ALPHABET
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

bp = Blueprint("user", __name__, url_prefix="/")


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = str(raw)
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


cipher = AESCipher("abcdefghijklmnopqrstuvwxyz")


@bp.route("/create", methods=["POST"])
@auth.login_required
def create():
    """
    Create user.
    """
    user = User(
        name=request.form.get("name"),
        email=request.form.get("email"),
        password=request.form.get("password")
    )

    db.session.add(user)
    db.session.commit()
    return cipher.encrypt("User Created"), 200


@bp.route("/retrieve/<id>", methods=["GET"])
@auth.login_required
def retrieve(id=None):
    """
    Retrieve the given user.
    """
    if id:
        q = db.session.query(User).filter(User.id == id)
        result = []
        for row in q:
            item = {
                "id": cipher.encrypt(row.id),
                "name": cipher.encrypt(row.name),
                "email": cipher.encrypt(row.email),
                "password": cipher.encrypt(row.password),
                "created": cipher.encrypt(row.created.strftime("%m/%d/%Y, %H:%M:%S"))
            }
            result.append(item)
        return jsonify(result)
    else:
        return cipher.encrypt("No ID Given")


@bp.route("/retrieve", methods=["GET"])
@auth.login_required
def retrieve_all():
    """
    Retrieve All users.
    """
    q = db.session.query(User).all()
    result = []
    for row in q:
        item = {
            "id": cipher.encrypt(row.id),
            "name": cipher.encrypt(row.name),
            "email": cipher.encrypt(row.email),
            "password": cipher.encrypt(row.password),
            "created": cipher.encrypt(row.created.strftime("%m/%d/%Y, %H:%M:%S"))
        }
        result.append(item)
    return jsonify(result)


@ bp.route("/delete/<id>", methods=["DELETE"])
@ auth.login_required
def delete(id=None):
    """
    Delete the given user.
    """
    if id:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return cipher.encrypt("OK"), 200
        else:
            return cipher.encrypt("Not Found")
    else:
        return cipher.encrypt("No ID Given")


@ bp.route("/update/<id>", methods=["PUT"])
@ auth.login_required
def update(id=None):
    """
    Update the given user.
    """
    if id:
        user = User.query.filter_by(id=id).first()
        if user:
            name = request.form.get("name", None)
            if name:
                user.name = name
            password = request.form.get("password", None)
            if password:
                user.password = password
            db.session.commit()
            return cipher.encrypt("OK"), 200
        else:
            return cipher.encrypt("Not Found")
    else:
        return cipher.encrypt("No ID Given")
