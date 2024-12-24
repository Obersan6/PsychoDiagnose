"""Forms for Diagnosis Tool"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError
from flask_wtf.file import FileField, FileAllowed 
from src.application.models import db, connect_db, User, Step, Sign, SignExample
from flask_wtf.file import FileField, FileAllowed


##############################################################################################
# CUSTOM VALIDATORS


def unique_username(form, field):
    """
    Validator to ensure unique username.
    
    Checks if the username already exists in the database and raises a ValidationError
    if it does.
    """
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('This username already exists, try another one.')

# Function to validate unique email field value
def unique_email(form, field):
    """
    Validator to ensure unique email.
    
    Checks if the email already exists in the database and raises a ValidationError
    if it does.
    """
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('This email already exists, try another one.')
    

##############################################################################################
# FORM CLASSES 


# Signup form
class SignupForm(FlaskForm):
    """Form to register a new user in the database."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)])
    username = StringField('Username', validators=[DataRequired(), unique_username, Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), unique_email, Length(max=254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    img_url = FileField('(Optional) Profile Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Register New User')
    

# Signin form
class SigninForm(FlaskForm):
    """Form for the user sing-in."""

    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Signin User')

# Update Profile Form
class UserProfileForm(FlaskForm):
    """For to update user's profile."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)])
    # Optional file upload
    img_url = FileField('(Optional) Update Profile Image', 
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # Optional remove image
    remove_image = BooleanField('Remove current image?')
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Update Profile')

# Step Form
class StepForm(FlaskForm):
    """Form to search for a diagnostic step."""
    
    search_query = StringField('Search Step', validators=[DataRequired()])
    submit = SubmitField('Search')


# Search Bar form
class SearchForm(FlaskForm):
    """Form with a single input field to search for elements."""

    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')








    




    


