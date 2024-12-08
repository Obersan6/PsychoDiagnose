from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User
from src.application.forms import SignupForm, SigninForm, UserProfileForm


user_bp = Blueprint('user', __name__, template_folder='templates/user') #CHECK IF I NEED TO REMOVE 'template_folder' since I didn't make subdirectories, this should be unnecessary.


#############################################################################
# User Routes

# @user_bp.before_request
# def add_user_to_g():
#     """If user is logged in, add current user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])
#         g.logged_in = True  # Set logged_in to True if a user is logged in
#     else:
#         g.user = None
#         g.logged_in = False  # Set logged_in to False if no user is logged in

# Signup route
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """"Handle user signup.
    - Create a new user.
    - If form not valid, show form.
    - If there already is a user with that 'username': flash message and show form again."""
    
    form = SignupForm()

    if form.validate_on_submit():
        try:
            new_user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,  
                img_url=form.img_url.data or None
            )
            db.session.commit()

        except IntegrityError:
            db.session.rollback() # Always roll back after and exception is raised
            flash('Username already exist. Please try again')
            return render_template('user/signup.html', form=form)
        
        session[CURR_USER_KEY] = new_user.id

        flash('Account created successfully! You are now logged in.')

        return redirect(url_for('homepage.homepage'))
    
    else:
        return render_template('user/signup.html', form=form)

# Signin route
@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Handle user login."""

    form = SigninForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
            flash(f"Hello, {user.username}!")
            return redirect(url_for('homepage.homepage'))
        
        flash('Invalid username or password.')
    
    return render_template('user/signin.html', form=form)


# logout route
@user_bp.route('/logout', methods=['POST'])
def logout():
    """Logout the current user."""

    session.pop(CURR_USER_KEY, None) # Removes only the current user's key from the session
    flash("You have been logged out.")
    return redirect(url_for('homepage.homepage'))

# User profile and update user profile route 
@user_bp.route('/user/<int:user_id>/profile', methods=['GET']) 
def user_profile(user_id):
    """Show user profile and edit user profile."""

    if not g.user:
        flash('Access unauthorized.')
        return redirect(url_for('user.signin'))
    
    return render_template('user/user_profile.html', user=g.user)

# Edit user profile route
@user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    """Edit current user profile."""
    
    # Ensure that g.user exists and matches the user_id
    if not g.user or g.user.id != user_id:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('user.signin'))

    user = g.user
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        # Temporarily remove password check for testing purposes
        print("Password verification skipped for testing.")

        # Update user fields
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.img_url = form.img_url.data or user.img_url  # Maintain current image if not provided

        try:
            # Commit changes to the database
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            print("Commit successful.")
            return redirect(url_for('user.user_profile', user_id=user.id))
        except Exception as e:
            # Handle errors during commit
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
            print("Commit failed. Exception:", e)
    else:
        print("Form validation failed with errors:", form.errors)  # Log form errors if validation fails

    return render_template('user/edit_profile.html', form=form, user=user)


# Delete user route 
@user_bp.route('/user/<int:user_id>/profile/delete', methods=['POST']) 
def delete_user_profile(user_id):
    """Delete user profile."""

    if not g.user:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('homepage.homepage'))
    
    logout()

    db.session.delete(g.user)
    db.session.commit()
    flash('User deleted', 'success')

    return redirect(url_for('homepage.homepage'))
    
