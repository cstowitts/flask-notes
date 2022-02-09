"""Flask app for Notes"""

from flask import Flask, render_template, redirect, session, flash

from models import db, User, connect_db

from forms import RegistrationForm, LoginForm

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
        Then redirect to /users/<username>
    """
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        session.pop("username", None)

        data = {k: v for k, v in register_form.data.items()
                if k != "csrf_token"}
        # not hurting but we are expliticly passing in things
        # could just do register_form.data

        new_user = User.register(
                   data['username'],
                   data['password'],
                   data['email'],
                   data['first_name'],
                   data['last_name'])

        username = new_user.username
        session["username"] = username
        db.session.add(new_user)
        db.session.commit()
        return redirect(f'/users/{username}')

    else:
        return render_template("register.html", form=register_form)


@app.route('/login', methods=["GET", "POST"])
def show_login_form():
    """GET: Show a form that when submitted will login a user.
        This form should accept a username and a password.

        POST: Process the login form,
        authenticate user and if so, redirect to /users/<username>
    """

    login_form = LoginForm()

    session.pop("username", None)

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.authenticate(username, password)
        if user:
            username = user.username
            session["username"] = username
            return redirect(f'/users/{username}')
    else:
        return render_template("login.html", form=login_form)


@app.get("/users/<username>")
def display_user_details(username):
    """Display a template that shows information
        about that user
        (everything except for their password)"""

    if "username" not in session or session["username"] != username:
        flash("You must be logged in to view")
        return redirect("/register")
    else:
        user = User.query.filter_by(username=username).one_or_none()
        return render_template("user.html", user=user)
