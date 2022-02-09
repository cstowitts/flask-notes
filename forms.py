from flask_wtf import FlaskForm

from wtforms import StringField

from wtforms.validators import InputRequired, Optional, Length


class RegistrationForm(FlaskForm):
    """Form to add new user"""

    username = StringField("Username",
                           validators=[InputRequired(), Length(max=20)])
    password = StringField("Password",
                           validators=[InputRequired(), Length(max=100)])
    email = StringField("Email",
                        validators=[InputRequired(), Length(max=50)])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name",
                             validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form to login"""

    username = StringField("Username",
                           validators=[InputRequired(), Length(max=20)])
    password = StringField("Password",
                           validators=[InputRequired(), Length(max=100)])
