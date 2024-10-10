from flask import request, Blueprint, render_template, redirect, url_for, flash
from utils.database import db
from models import User
from sqlalchemy.exc import IntegrityError

user_blueprint = Blueprint('user_controller', __name__)

# Get all users
@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Create a new user (GET for form, POST for form submission)
@user_blueprint.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('add_user.html')  # Show the form to the user

    elif request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Create the new user
            user = User(
                username=username,
                email=email,
                password=password  # Store the plain password for simplicity; consider hashing for security
            )
            db.session.add(user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('user_controller.get_users'))  # Redirect after successful creation
        except IntegrityError:
            db.session.rollback()
            flash('Error: Username or email already exists.', 'danger')
            return render_template('add_user.html'), 400

# Update a user (GET for form, POST for form submission)
@user_blueprint.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get(id)

    if request.method == 'GET':
        return render_template('edit_user.html', user=user)  # Show the edit form pre-filled with the user's data

    elif request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Only update password if provided
        if password:
            user.password = password

        # Handle empty form fields by keeping old data
        user.username = username if username else user.username
        user.email = email if email else user.email
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('user_controller.get_users'))

# Delete a user
@user_blueprint.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('user_controller.get_users'))  # Redirect after successful deletion
