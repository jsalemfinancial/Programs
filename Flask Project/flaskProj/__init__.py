from flask import Flask, session
from flask_bcrypt import Bcrypt

app = Flask(__name__.split(".")[0])
app.config["dbConfig"] = {"host": "flaskdb-001.cmtvzzpoedvj.us-east-2.rds.amazonaws.com", "port": "5050", "user": "flaskadmin", "password": "flasklover", "database": "flaskDBz"}
app.config["SECRET_KEY"] = "BiGGiEsmaLLz555313555baCKaTiTaGaIN"

flaskBcrypt = Bcrypt(app)

from flaskProj import routes