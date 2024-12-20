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


user_bp = Blueprint('user', __name__, template_folder='templates/user') #CHECK IF I NEED TO REMOVE 'template_folder' since I didn't make subdirectories, this should be unnecessary.



#############################################################################
# User Routes


# Signup route
# @user_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     img_file = form.img_url.data
#     img_path = None # Default to None

#     if form.validate_on_submit():
#         # Save the file if valid
#         if img_file and allowed_file(img_file.filename):
#             img_path = save_file(current_app.config['UPLOAD_FOLDER'], img_file)
        # else remains None

        # try: BELOW THIS LINE ANOTHER VERSION
            # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # new_user = User(
            #     first_name=form.first_name.data,
            #     last_name=form.last_name.data,
            #     username=form.username.data,
            #     email=form.email.data,
            #     password_hash=hashed_password,
            #     img_url=img_path  # Save None if no image uploaded
            # )
            # db.session.add(new_user)
            # User.signup(
            # username=form.username.data,
            # email=form.email.data,
            # first_name=form.first_name.data,
            # last_name=form.last_name.data,
            # password=form.password.data,
            # img_url=img_path  # Pass None or uploaded file path
            # )
            # Pass None if no image is uploaded
            # ABOVE THIS LINE ANOTHER VERSION OF USER
    #         new_user = User.signup(
    #             username=form.username.data,
    #             email=form.email.data,
    #             first_name=form.first_name.data,
    #             last_name=form.last_name.data,
    #             password=form.password.data,
    #             img_url=img_path if img_path else None
    #         )
    #         db.session.commit()
    #         session[CURR_USER_KEY] = new_user.id
    #         flash('Account created successfully!')
    #         return redirect(url_for('homepage.homepage'))

    #     except IntegrityError:
    #         db.session.rollback()
    #         flash('Username already exists. Please try again.')

    # return render_template('user/signup.html', form=form)

# @user_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     img_file = form.img_url.data
#     img_path = None # Default to None

#     if form.validate_on_submit():
#         # Save the file if valid
#         if img_file and allowed_file(img_file.filename):
#             img_path = save_file(current_app.config['UPLOAD_FOLDER'], img_file)
#         # else:
#         #    img_path = None  # Explicitly set to None if no image is uploaded

#         try:
#             new_user = User.signup(
#                 username=form.username.data,
#                 email=form.email.data,
#                 first_name=form.first_name.data,
#                 last_name=form.last_name.data,
#                 password=form.password.data,
#                 img_url=img_path if img_path else None
#             )
#             db.session.commit()
#             session[CURR_USER_KEY] = new_user.id
#             flash('Account created successfully!')
#             return redirect(url_for('homepage.homepage'))

#         except IntegrityError:
#             db.session.rollback()
#             flash('Username already exists. Please try again.')

#     return render_template('user/signup.html', form=form)  

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
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

        # Default image if no file is uploaded
        if not img_path:
            img_path = "/static/uploads/default.jpg"

        try:
            new_user = User.signup(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data,
                img_url=img_path
            )
            db.session.commit()
            session[CURR_USER_KEY] = new_user.id
            flash('Account created successfully!', 'success')
            return redirect(url_for('homepage.homepage'))

        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please try again.', 'danger')

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
# @user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
# def edit_profile(user_id):
#     """Edit current user profile."""
    
#     # Ensure that g.user exists and matches the user_id
#     if not g.user or g.user.id != user_id:
#         flash('Access unauthorized', 'danger')
#         return redirect(url_for('user.signin'))

#     user = g.user
#     form = UserProfileForm(obj=user)

#     if form.validate_on_submit():
#         # Temporarily remove password check for testing purposes
#         print("Password verification skipped for testing.")

#         # Update user fields
#         user.first_name = form.first_name.data
#         user.last_name = form.last_name.data
#         user.img_url = form.img_url.data or user.img_url  # Maintain current image if not provided

#         # THIS WAS COMMENTED OUT BEFORE THE REST OF THE ROUT
#         # if form.remove_image.data:
#         #     user.img_url = None
#         # else:
#         #     # The user might have uploaded a new file
#         #     img_file = form.img_url.data
#         #     if img_file and allowed_file(img_file.filename):
#         #         new_path = save_file(current_app.config['UPLOAD_FOLDER'], img_file)
#         #         user.img_url = new_path
#         #     # If no file was uploaded, we keep the existing user.img_url



#         try:
#             # Commit changes to the database
#             db.session.commit()
#             flash('Profile updated successfully!', 'success')
#             print("Commit successful.")
#             return redirect(url_for('user.user_profile', user_id=user.id))
#         except Exception as e:
#             # Handle errors during commit
#             db.session.rollback()
#             flash('Error updating profile. Please try again.', 'danger')
#             print("Commit failed. Exception:", e)
#     else:
#         print("Form validation failed with errors:", form.errors)  # Log form errors if validation fails

#     return render_template('user/edit_profile.html', form=form, user=user)

# @user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
# def edit_profile(user_id):
#     """Edit current user profile."""
#     if not g.user or g.user.id != user_id:
#         flash('Access unauthorized', 'danger')
#         return redirect(url_for('user.signin'))

#     user = g.user
#     form = UserProfileForm(obj=user)

#     if form.validate_on_submit():
#         # Update user fields
#         user.first_name = form.first_name.data
#         user.last_name = form.last_name.data

#         # Handle image upload
#         if form.img_url.data and hasattr(form.img_url.data, 'filename'):
#             # Define upload folder
#             upload_folder = os.path.join('static', 'uploads')
#             if not os.path.exists(upload_folder):
#                 os.makedirs(upload_folder)

#             # Save uploaded file
#             filename = secure_filename(form.img_url.data.filename)
#             image_path = os.path.join(upload_folder, filename)
#             form.img_url.data.save(image_path)

#             # Save relative path to database
#             user.img_url = f'uploads/{filename}'

#         # Handle image removal
#         if 'remove_image' in request.form:
#             # Optionally delete the file from the server
#             if user.img_url:
#                 image_path = os.path.join('static', user.img_url)
#                 if os.path.exists(image_path):
#                     os.remove(image_path)

#             user.img_url = None

#         try:
#             # Commit changes to the database
#             db.session.commit()
#             flash('Profile updated successfully!', 'success')
#             return redirect(url_for('user.user_profile', user_id=user.id))
#         except Exception as e:
#             db.session.rollback()
#             flash('Error updating profile. Please try again.', 'danger')
#             print("Commit failed. Exception:", e)

#     return render_template('user/edit_profile.html', form=form, user=user)

# @user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
# def edit_profile(user_id):
#     """Edit current user profile."""
    
#     # Ensure that g.user exists and matches the user_id
#     if not g.user or g.user.id != user_id:
#         flash('Access unauthorized', 'danger')
#         return redirect(url_for('user.signin'))

#     user = g.user
#     form = UserProfileForm(obj=user)

#     if form.validate_on_submit():
#         # Update user fields
#         user.first_name = form.first_name.data
#         user.last_name = form.last_name.data

#         # Handle image upload
#         if form.img_url.data:
#             # Save the uploaded file to a directory (e.g., 'static/uploads')
#             image_path = f'static/uploads/{form.img_url.data.filename}'
#             form.img_url.data.save(image_path)
#             user.img_url = image_path  # Update with the new file path

#         # Handle image removal (e.g., checkbox in the form to remove image)
#         if 'remove_image' in request.form:
#             user.img_url = None

#         try:
#             # Commit changes to the database
#             db.session.commit()
#             flash('Profile updated successfully!', 'success')
#             return redirect(url_for('user.user_profile', user_id=user.id))
#         except Exception as e:
#             db.session.rollback()
#             flash('Error updating profile. Please try again.', 'danger')
#             print("Commit failed. Exception:", e)

#     return render_template('user/edit_profile.html', form=form, user=user)



@user_bp.route('/user/<int:user_id>/profile/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    """Edit current user profile."""
    if not g.user or g.user.id != user_id:
        flash('Access unauthorized', 'danger')
        return redirect(url_for('user.signin'))

    user = g.user
    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        # Update user fields
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        # Handle image upload
        if form.img_url.data and hasattr(form.img_url.data, 'filename'):
            # Define upload folder
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Remove old image if it exists
            if user.img_url:
                old_image_path = os.path.join('static', user.img_url)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save uploaded file
            filename = secure_filename(form.img_url.data.filename)
            image_path = os.path.join(upload_folder, filename)
            form.img_url.data.save(image_path)

            # Save relative path to database
            user.img_url = f'uploads/{filename}'

        # Handle image removal
        if 'remove_image' in request.form:
            if user.img_url:
                old_image_path = os.path.join('static', user.img_url)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            user.img_url = None

        try:
            # Commit changes to the database
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.user_profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'danger')
            print("Commit failed. Exception:", e)

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
    
