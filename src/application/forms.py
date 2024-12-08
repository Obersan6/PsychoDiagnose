"""Forms for Diagnosis Tool"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError
from src.application.models import db, connect_db, User, Step, Sign, SignExample

##############################################################################################
# CUSTOM VALIDATORS

# Function to validate unique username field value
def unique_username(form, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('This username already exists, try another one.')

# Function to validate unique email field value
def unique_email(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('This email already exists, try another one.')

##############################################################################################
# FORM CLASSES 

# Signup form
class SignupForm(FlaskForm):
    """Form that will add a new user to the db."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)])
    username = StringField('Username', validators=[DataRequired(), unique_username, Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), unique_email, Length(max=254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    img_url = StringField('(Optional) Image URL', validators=[Optional(), URL()])
    submit = SubmitField('Register New User')

class SigninForm(FlaskForm):
    """Form for the user to sing-in."""

    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Signin User')

class UserProfileForm(FlaskForm):
    """For to update user's profile."""

    first_name = StringField('First Name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=150)])
    img_url = StringField('(Optional) Image URL', validators=[Optional(), URL()])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Update Profile')

class StepForm(FlaskForm):
    "Form to retrieve a Dianostic Step."

    ### NEW VERSION OF THE FORM ONLY ONE FIELD FOR BOTH
    
    search_query = StringField('Search Step', validators=[DataRequired()])
    submit = SubmitField('Search')

    # step_number = IntegerField('Step Number', validators=[Optional()])
    # step_name = StringField('Step Name', validators=[Optional(), Length(max=150)])
    # submit = SubmitField('Search')

    # def validate(self):
    #     """Custom validation to ensure at least one field is filled"""

    #     if not super(StepForm, self).validate():
    #         return False
        
    #     if not self.step_number.data and not self.step_name.data:
    #         error_message = 'Please enter either step number or step name'
    #         self.step_number.errors.append(error_message)
    #         self.step_name.errors.append(error_message)
    #         return False
        
    #     return True

# Look for a sign input form
# OLGA REMEMBER TO CHANGE THIS NAME HERE AND EVERYWHERE IN THE APPLICATION 
class SearchForm(FlaskForm):
    """One input form to search for an element."""

    search_query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')








    




    


