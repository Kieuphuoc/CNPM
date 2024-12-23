from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "bgaydfas6da$#%@sdfadfa@@"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/clinicdb?charset=utf8mb4" % quote('mysql')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
login = LoginManager(app)

cloudinary.config(
        cloud_name='dpfbtypxx',
        api_key='191724613981669',
        api_secret='4fgFs1HJMoFsbFnaG61IMCW10IM',
        secure=True
)
