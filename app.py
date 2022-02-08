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
    """GET: displays registration form to create a user
        This form should accept a username, password,
        email, first_name, and last_name.

        POST: Process the registration form by adding a new user.
        Then redirect to /secret
    """
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        data = {k: v for k, v in register_form.data.items() if k!= "csrf_token"}
        #buggy? check back
    
        new_user = User.register(
                   data['username'],
                   data['password'],
                   data['email'],
                   data['first_name'],
                   data['last_name'])

        db.session.add(new_user)
        db.session.commit()
        return redirect('/secret')

    #     new_user = User(**data)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect('/secret')
    # else:
    #     return render_template("register.html", form=register_form)

   




@app.route('/login', methods=["GET", "POST"])
def login():
    """GET: Show a form that when submitted will login a user.
        This form should accept a username and a password.

        POST: Process the login form, 
        authenticate user and if so, redirect to /secret
    """

    login_form = LoginForm()

    if login_form.validate_on_submit():

