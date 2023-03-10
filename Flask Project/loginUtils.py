from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class loginPortal(FlaskForm):
    userEmail = StringField("E-mail:", validators=[DataRequired(), Email(check_deliverability=True)])
    userPassword = PasswordField("Password:", validators=[DataRequired(), Length(min=8, max=32)])
    submitButton = SubmitField("Send Data")