from app import app, login_manager
from models import db, User
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, redirect, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField()

@app.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    all_records = ""
    #Connect to MongoDB
    try:
        client = MongoClient("mongodb+srv://admin:eCCvjBufsXE7RnzH@cluster0.r8alamr.mongodb.net/?retryWrites=true&w=majority") 
        db = client.maindb.info
        all_records = db.find()
        flash("Connected to MongoDB", 'success')
    except Exception as e:
        flash("Failed to establish connection to MongoDB", 'danger')
        print(str(e))

    if request.method == 'GET':
        if request.args.get('option') == "remove":
            item_uuid = request.args.get('uuid')
            try:
                db.delete_one({"notification_id": request.args.get('uuid')})
                flash("Item deleted!", 'danger')
            except Exception as e:
                flash("Cannot delete object!" + str(e), 'danger')
    return render_template('dashboard.html', records=all_records)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user)
            flash("Authenticated!", 'success')
            return redirect('/')
        else:
            db.session.rollback()
            flash("Incorrect Username or Password", 'danger')
            return redirect('/login')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = User(username=form.username.data, hashed_password=bcrypt.generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            flash("User created!", 'success')
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            flash(f"Error occurred!, {str(e)}", 'danger')
            return redirect('/register')
    return render_template('register.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged Out!", 'info')
    return redirect('/login')
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    