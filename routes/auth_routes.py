from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.user_model import Customer, User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists!')
            return redirect(url_for('auth.register'))
        
        new_customer = Customer(name=name, email=email)
        new_customer.set_password(password)
        
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Account Created! Please Login.')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return "<h1>Login Successful! (System Working)</h1>"
        else:
            flash('Login Failed. Check email or password.')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged Out Successfully"