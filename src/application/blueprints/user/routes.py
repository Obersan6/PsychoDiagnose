from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User
from src.application.forms import SignupForm, SigninForm, UserProfileForm
from src.application.utils.file_utils import allowed_file, save_file
from flask import current_app
from src.application.models import db, connect_db, User, bcrypt
from werkzeug.utils import secure_filename
import os


user_bp = Blueprint('user', __name__, template_folder='templates/user') 


#############################################################################
# User Routes


# User signup 
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user signup.
    - GET: Display the signup form.
    - POST: Validate the form, create a new user, handle image upload, and log the user in.
    - Redirects to the homepage upon success or flashes errors for issues like duplicate usernames/emails.
    """
    form = SignupForm()
    img_file = form.img_url.data
    img_path = None  # Default to None

    if form.validate_on_submit():
        # Handle image upload
        if img_file and allowed_file(img_file.filename):
            try:
                upload_folder = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Save the image file
                filename = secure_filename(img_file.filename)
                img_file.save(os.path.join(upload_folder, filename))

                # Set the relative path for the image
                img_path = f"uploads/{filename}"
            except Exception as e:
                flash(f"Image upload failed: {e}", 'danger')

        # Assign default image if no file is provided
        if not img_path:
            img_path = "/static/uploads/default.jpg"

        try:
            # Create a new user and commit to the database
            new_user = User.signup(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                img_url=img_path
            )
            db.session.commit()
            session[CURR_USER_KEY] = new_user.id # Log the user in
            flash('Account created successfully!', 'success')
            return redirect(url_for('homepage.homepage'))

        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please try again.', 'danger')

    return render_template('user/signup.html', form=form)


# User signin 
@user_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    Handle user login.
    - GET: Display the login form.
    - POST: Authenticate the user and log them in.
    - Redirects to the homepage if successful or flashes errors for invalid credentials.
    """

    form = SigninForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
            flash(f"Hello, {user.username}!")
            return redirect(url_for('homepage.homepage'))
        
        flash('Invalid username or password.')
    
    return render_template('user/signin.html', form=form)


# User logout 
@user_bp.route('/logout', methods=['POST'])
def logout():
    """
    Handle user logout.
    - Logs out the current user by clearing their session.
    - Redirects to the homepage after logout.
    """

    session.pop(CURR_USER_KEY, None) 
    flash("You have been logged out.")
    return redirect(url_for('homepage.homepage'))

# User profile  
@user_bp.route('/user/<int:user_id>/profile', methods=['GET']) 
def user_profile(user_id):
    """
    Display the logged-in user's profile.
    - Ensures the user is logged in before rendering the profile page.
    - Redirects to the signin page if unauthorized.
    """

    if not g.user:
        flash('Access unauthorized.')
        return redirect(url_for('user.signin'))
    
    return render_template('user/user_profile.html', user=g.user)

# Edit user profile 
@user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    """
    Handle user profile editing.
    - GET: Display the profile editing form.
    - POST: Update user information, including name and image, with options for image upload or removal.
    - Ensures only the logged-in user can edit their profile.
    """
    if not g.user or g.user.id != user_id:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('user.signin'))

    user = g.user
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        # Update user's name and last name
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        # Handle image upload or replacement
        if form.img_url.data and hasattr(form.img_url.data, 'filename'):
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Remove old image if it exists
            if user.img_url:
                old_image_path = os.path.join('static', user.img_url)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save uploaded image
            filename = secure_filename(form.img_url.data.filename)
            image_path = os.path.join(upload_folder, filename)
            form.img_url.data.save(image_path)
            user.img_url = f'uploads/{filename}'

        # Handle image removal
        if 'remove_image' in request.form:
            if user.img_url:
                old_image_path = os.path.join('static', user.img_url)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            user.img_url = None

        try: 
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.user_profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
            print("Commit failed. Exception:", e)

    return render_template('user/edit_profile.html', form=form, user=user)

# Delete user  
@user_bp.route('/user/<int:user_id>/profile/delete', methods=['POST']) 
def delete_user_profile(user_id):
    """
    Handle user profile deletion.
    - Ensures only the logged-in user can delete their profile.
    - Logs out the user, deletes their account, and redirects to the homepage.
    """

    if not g.user:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('homepage.homepage'))
    
    logout()

    db.session.delete(g.user) 
    db.session.commit()
    flash('User deleted', 'success')

    return redirect(url_for('homepage.homepage'))
    
