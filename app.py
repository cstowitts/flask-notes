"""Flask app for Notes"""

from flask import Flask, render_template, redirect

from models import db, User, connect_db

from forms import RegistrationForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Steve's_BAD_Knees"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def redirect_to_register():
    """redirects to register"""
    
    return redirect("/register")

@app.route('/register', methods=["GET", "POST"])
def show_registration_form():
    """displays registration form to create a user
        This form should accept a username, password,
        email, first_name, and last_name.
    """
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        data = {k:v for k, v in register_form.data.items() if k!= "csrf_token"}
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
    else:
        return render_template("register.html", form=register_form)
