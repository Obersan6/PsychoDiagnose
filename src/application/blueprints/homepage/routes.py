"""Homepage route"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
from src.application.models import db, connect_db, User, Sign, Symptom, Step, Category, Cluster, Disorder
from src.application.forms import SearchForm
from src.config import CURR_USER_KEY
from sqlalchemy import func
import os


# Define an absolute path for the template folder
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main/templates/homepage'))
print("Template path for homepage_bp:", template_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_path)


#############################################################################
# ROUTES

# Homepage
@homepage_bp.route('/', methods=['GET'])
def homepage():
    """
    Renders the homepage.
    - Displays a different view depending on whether the user is logged in or not.
    - Provides access to login, signup, or personalized features.
    """
    print("Rendering homepage route.")
    print("Is user logged in:", bool(g.user))
    try:
        return render_template(
            'home.html',
            user_logged_in=bool(g.user),
            user=g.user if g.user else None
        )
    except Exception as e:
        print("Error rendering template:", str(e))
        raise
