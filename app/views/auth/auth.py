from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, mail
from app.models.user import User
from app.forms import RegistrationForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"User found: {user.username}")
            if check_password_hash(user.password, form.password.data):
                print("Password is correct")
                login_user(user)
                return redirect(url_for('dashboard.show_dashboard'))
            else:
                print("Incorrect password")
        else:
            print("No user found with that email")
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.show_dashboard'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.show_dashboard'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('dashboard.show_dashboard'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)

def send_password_reset_email(user):
    try:
        token = user.get_reset_password_token()
        msg = Message('Reset Your Password',
                      sender='hola@aztros.com',
                      recipients=[user.email])
        msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
        with mail.connect() as conn:
            conn.send(msg)
        print("Correo enviado con éxito a:", user.email)
    except Exception as e:
        print("Error al enviar el correo:", e)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
