"""Homepage route"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
from src.application.models import db, connect_db, User, Sign, Symptom, Step, Category, Cluster, Disorder
from src.application.forms import SearchForm
from src.config import CURR_USER_KEY
from sqlalchemy import func
import os

# homepage_bp = Blueprint('homepage', __name__, template_folder='../../main/templates/homepage')

# Define an absolute path for the template folder
template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../main/templates/homepage'))
print("Template path for homepage_bp:", template_path)

homepage_bp = Blueprint('homepage', __name__, template_folder=template_path)


#############################################################################
# BEFORE REQUEST

# @homepage_bp.before_request
# def add_user_to_g():
#     """If user is logged in, add current user to Flask global for homepage routes."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])
#         g.logged_in = True # Set logged_in to True if a user is logged in
#     else:
#         g.user = None
#         g.logged_in = False # Set logged_in to False if no user is logged in

############################################################################### 
# ROUTE

# Homepage 
# THIS ROUTE ISN'T FINISHED YET!!!!!
# @homepage_bp.route('/', methods=['GET', 'POST'])
# def homepage():
#     """Home page.
#     - If user is logged out show signed-out homepage (home.html).
#     - If user is logged in show signed-in homepage(home.html) with user details on the side; and similar content to the other one."""
    
#     form = SearchForm()

#     if g.user:
#         # Pass img_url as is, since it defaults to None
#         img_url = g.user.img_url if g.user.img_url and g.user.img_url.strip() != "" else None
#         # Process form submission
#         if form.validate_on_submit():
#             search_query = form.search_query.data.strip()
#             return redirect(url_for('homepage.search', query=search_query))
        
#         # Pass the logged-in user's info and form to the template
#         return render_template(
#             'home.html',
#             user_logged_in=True,
#             username=g.user.username,
#             # img_url=g.user.img_url,
#             img_url=img_url,
#             form=form
#         )
#     else:
#         # Render template without form or user details for logged-out users
#         return render_template('home.html', user_logged_in=False)

# @homepage_bp.route('/')
# def homepage():
#     """Render the homepage."""
#     form = SearchForm()
#     if g.logged_in:  # Check if the user is logged in
#         print(f"DEBUG: img_url={g.user.img_url}")  # Debugging line
#         img_url = g.user.img_url if g.user.img_url and g.user.img_url.strip() != "" else None
#         return render_template(
#             'homepage/home.html',
#             user_logged_in=True,
#             user=g.user,  # Pass the 'g.user' object to the template
#             form=form,
#             img_url=img_url
#         )
#     else:
#         return render_template(
#             'homepage/home.html',
#             user_logged_in=False
#         )

# Previous homepage that worked with search bar
# @homepage_bp.route('/', methods=['GET', 'POST'])
# def homepage():
#     """Home page.
#     - If user is logged out, show signed-out homepage (home.html).
#     - If user is logged in, show signed-in homepage with user details and a search form."""
    
#     form = SearchForm()

#     if g.user:
#         # Process form submission
#         if form.validate_on_submit():
#             search_query = form.search_query.data.strip()
#             return redirect(url_for('homepage.search', query=search_query))

#         # Pass the user object and form to the template
#         return render_template(
#             'home.html',
#             user_logged_in=True,
#             user=g.user,  # Pass the entire user object
#             form=form
#         )
#     else:
#         # Render template without form or user details for logged-out users
#         return render_template('home.html', user_logged_in=False)

#  this one works
@homepage_bp.route('/', methods=['GET'])
def homepage():
    """Home page.
    - If user is logged out, show signed-out homepage (home.html).
    - If user is logged in, show signed-in homepage with user details."""
    
    if g.user:
        # Pass the user object to the template
        return render_template(
            'home.html',
            user_logged_in=True,
            user=g.user  # Pass the entire user object
        )
    else:
        # Render template without user details for logged-out users
        return render_template('home.html', user_logged_in=False)


# Search form to search for most of the elements of the application
@homepage_bp.route('/search', methods=['GET'])
def search():
    """Handle the search form submission and search across models for an exact match."""
    
    query = request.args.get('query', '').strip()

    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('homepage.homepage'))
    
    # Define models to search, specifying (Model, Blueprint Name, Route Name, Field)
    search_models = [
        (Sign, 'psychopathology_bp', 'get_sign', 'name'),
        (Symptom, 'psychopathology_bp', 'get_symptom', 'name'),
        (Step, 'dsm_bp', 'get_step', 'name_or_number'),
        (Category, 'dsm_bp', 'get_category', 'name'),
        (Cluster, 'dsm_bp', 'get_cluster', 'name')
        (Disorder, 'dsm_bp', 'get_disorder', 'name')
    ]

    matched_item = None
    matched_blueprint = None
    matched_route = None

    for model, blueprint, route, field in search_models:
        if model.__name__ == 'Step' and field == 'name_or_number':
            # For Steps, match either by name or number
            match_by_name = model.query.filter(func.lower(model.step_name) == query.lower()).first()
            match_by_number = model.query.filter(model.step_number == int(query)).first() if query.isdigit() else None
            
            # Set matched_item to the first non-None match
            matched_item = match_by_name or match_by_number
        else:
            # For other models, match by name only
            matched_item = model.query.filter(func.lower(getattr(model, field)) == query.lower()).first()

        if matched_item:
            matched_blueprint = blueprint
            matched_route = route
            break  # Stop searching once a match is found

    # Ensure matched_item has been found and has an id attribute before redirecting
    if matched_item and hasattr(matched_item, 'id'):
        return redirect(url_for(f'{matched_blueprint}.{matched_route}', id=matched_item.id))
    else:
        flash(f"No exact match found for '{query}'. Please try again.", "warning")
        return redirect(url_for('homepage.homepage'))


