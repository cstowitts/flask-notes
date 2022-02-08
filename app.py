"""Flask app for Notes"""

from flask import Flask, render_template, redirect

from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Steve's_BAD_Knees"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_register():
    """redirects to register"""
    
    return redirect("/register")

@app.get('/register')
def show_registration_form():
    """displays registration form to create a user
        This form should accept a username, password,
        email, first_name, and last_name.
    """

