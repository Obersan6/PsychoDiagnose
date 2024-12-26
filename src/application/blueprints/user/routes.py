from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session, current_app
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User
from src.application.forms import SignupForm, SigninForm, UserProfileForm
from src.application.utils.file_utils import allowed_file, save_file
from flask import current_app
from src.application.models import db, connect_db, User, bcrypt
from werkzeug.utils import secure_filename
import os
import uuid 
from uuid import uuid4 



user_bp = Blueprint('user', __name__, template_folder='templates/user') 
my_blueprint = Blueprint('my_blueprint', __name__)


#############################################################################
# User Routes


# User signup 
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handle user signup:
    - GET: Render the signup form.
    - POST: Create a new user with the provided details and log them in.
    - Handles image uploads for the user's profile picture, setting a default image if none is provided.
    - Redirects to the homepage after successful signup or flashes an error for invalid data.
    """
    form = SignupForm()
    img_file = form.img_url.data
    img_path = "uploads/default.jpg"  # Default image path

    if form.validate_on_submit():
        if img_file and allowed_file(img_file.filename):
            try:
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)

                # Save the uploaded image with a unique filename
                filename = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
                img_file.save(os.path.join(upload_folder, filename))
                img_path = f"uploads/{filename}"  # Set the database path

            except Exception as e:
                flash(f"Image upload failed: {e}", 'danger')

        try:
            # Create a new user in the database
            new_user = User.signup(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                img_url=img_path
            )
            db.session.commit()
            session[CURR_USER_KEY] = new_user.id  # Log the user in
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
    Handle user profile editing:
    - GET: Render the profile editing form pre-filled with the user's current details.
    - POST: Update the user's profile information (name and profile picture).
    - Handles image uploads with unique filenames and allows image removal.
    - Redirects to the user's profile page after a successful update or flashes an error if something goes wrong.
    - Ensures that only the logged-in user can edit their profile.
    """
    if not g.user or g.user.id != user_id:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('user.signin'))

    user = g.user
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        # Update user's first name and last name
        user.first_name = form.first_name.data or user.first_name
        user.last_name = form.last_name.data or user.last_name

        # Handle image upload
        img_file = form.img_url.data
        img_path = user.img_url or 'uploads/default.jpg'

        if img_file and hasattr(img_file, 'filename') and allowed_file(img_file.filename):
            try:
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)

                # Save new image with a unique filename
                filename = f"{uuid.uuid4().hex}_{secure_filename(img_file.filename)}"
                img_file.save(os.path.join(upload_folder, filename))
                img_path = f"uploads/{filename}"

                # Remove old image if applicable
                if user.img_url and user.img_url != 'uploads/default.jpg':
                    old_image_path = os.path.join(current_app.root_path, 'static', user.img_url)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

            except Exception as e:
                flash(f"Image upload failed: {e}", 'danger')

        # Handle image removal
        elif 'remove_image' in request.form:
            if user.img_url and user.img_url != 'uploads/default.jpg':
                old_image_path = os.path.join(current_app.root_path, 'static', user.img_url)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            img_path = 'uploads/default.jpg'

        # Update the user profile with new details
        user.img_url = img_path

        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.user_profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile. Please try again. ({e})", 'danger')

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
    
