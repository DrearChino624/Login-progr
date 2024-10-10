from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from utils.database import db
from flask_login import LoginManager
from models import User

# Initialize Blueprint
login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/', methods=['GET', 'POST'])
def login(): 
    
    if current_user.is_authenticated:
        return redirect(url_for('user_controller.get_users'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print("Usuario no encontrado")  # Si el usuario no existe
        else:
            print(f"Usuario encontrado: {user.username}")
            print(f"Usuario encontrado: {user.email}")
            print(f"Hash almacenado: {user.password}")
            print(f"Contraseña ingresada: {password}")

        # Check if user exists and password is correct
        if user:
            print("Entrando en la función check") 
            login_user(user)
            return render_template('users.html', users=User.query.all())
        else:
            print("Entrando en la función error") 
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))
