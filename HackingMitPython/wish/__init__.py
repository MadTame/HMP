from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER437444_tame:hmp_hs-albsig@tamemarc.lima-db.de:3306/db_437444_2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f1c50cdf58a5ac7024799455'

db = SQLAlchemy(app)

from wish import routes