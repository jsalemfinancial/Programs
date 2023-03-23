from functools import wraps
from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from flaskProj import app, session
from flaskProj.dbUtils import DBCommands

class loginPortal(FlaskForm):
    userEmail = StringField("E-mail:", validators=[DataRequired(), Email(check_deliverability=True)])
    userPassword = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=32)])
    submitButton = SubmitField("Send Data")

    def sessionStatus(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if ("logged_in") in session:
                return function(*args, **kwargs)
            
            return redirect(url_for("login"))
        
        return wrapper
    
    def validate_userEmail(self, userEmail):
        with DBCommands(app.config["DB_CONFIG"]) as cursor:
            cursor.execute("""SELECT email
                                FROM userAccounts
                                WHERE email=%s""", (str(userEmail.data).lower(),)) #Extra ',' at end to tell python to unpack tuple.
            result = cursor.fetchone()

        if (result):
            raise ValidationError("Email already registered.")