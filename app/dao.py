from app.models import User, BenhNhan, Thuoc
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user


def get_user_by_id(id):
    return User.query.get(id)


def load_patients(kw=None):
    query = BenhNhan.query

    if kw:
        query = query.filter(BenhNhan.name.contains(kw))

    return query.all()


def load_medicines(kw=None):
    query = Thuoc.query

    if kw:
        query = query.filter(Thuoc.name.contains(kw))

    return query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))
    return u.first()



