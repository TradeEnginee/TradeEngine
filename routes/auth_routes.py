from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Database.Repositories.user_repo import UserRepository
from models.user_model import Customer, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            mobile = request.form['mobile']
            

            new_customer = Customer(None, username, email, None, mobile, "{}")
            

            new_customer.password = password
            

            if UserRepository.add_user(new_customer):
                flash("Account created successfully! Please login.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Error: Username or Email already exists.", "error")
                
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = UserRepository.get_user_by_email(email)
        

        if user and user.verify_password(password):
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f"Welcome back, {user.username}!", "success")
            

            return redirect(url_for('shop.home')) 
            
        else:
            flash("Invalid email or password!", "error")
            
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))