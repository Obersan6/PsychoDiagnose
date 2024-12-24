from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
# from flask_login import login_required 
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User, Sign, SignExample, Disorder,  DisorderSign, Symptom, SymptomExample, DisorderSymptom
from src.application.forms import SearchForm
# from src.application.forms import 

psychopathology_bp = Blueprint('psychopathology', __name__, template_folder='templates/psychopathology')

#############################################################################
# PSYCHOPATHOLOGY ITEMS 

# List of all signs
@psychopathology_bp.route('/signs', methods=['GET'])
def show_signs():
    """
     Display a list of all signs.
    - Accessible only to logged-in users.
    - Includes a search form for user convenience.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    signs = Sign.query.order_by(Sign.name.asc()).all()
    form = SearchForm()

    return render_template('psychopathology/signs.html', signs=signs, form=form)

# Search for a sign
@psychopathology_bp.route('/signs/search', methods=['POST'])
def search_sign():
    """
    Handle search functionality for signs.
    - Supports searches by ID (numeric input) or name (string input).
    - Redirects to the specific sign's page if a match is found.
    - Displays an error message if no match is found or input is invalid.
    """
    
    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        # Search by ID or name
        if search_query.isdigit():
            sign = Sign.query.filter_by(id=int(search_query)).first()
        else:
            sign = Sign.query.filter(Sign.name.ilike(f"%{search_query}%")).first()
        
        # If there is a match, redirect to sign's page
        if sign:
            return redirect(url_for('psychopathology.get_sign', sign_id=sign.id))
        
        flash('Please enter a valid term', 'dange')
        return redirect(url_for('psychopathology.show_signs'))

# Autocomplete suggestions for sign search
@psychopathology_bp.route('/signs/autocomplete', methods=['GET'])
def autocomplete_sign():
    """
    Provide a JSON list of sign names matching the user's input.
    - Matches are case-insensitive.
    - Returns an empty list if no input is provided or no matches are found.
    """

    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])
    
    matching_signs = Sign.query.filter(Sign.name.ilike(f"{query}%")).all()
    sign_names = [sign.name for sign in matching_signs]

    return jsonify(sign_names)

# Sign details
@psychopathology_bp.route('/signs/<int:sign_id>', methods=['GET'])
def get_sign(sign_id):
    """
    Display details of a specific sign.
    - Includes the sign's description, associated examples, 
      and related disorders with this sign.
    - Accessible only to logged-in users.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    sign = Sign.query.get_or_404(sign_id)
    form = SearchForm()

    # Retrieve disorders associated with this sign 
    disorders = (
        Disorder.query
        .join(DisorderSign, Disorder.id == DisorderSign.disorder_id)
        .filter(DisorderSign.sign_id == sign.id)
        .all()
    )

    return render_template(
        'psychopathology/sign.html', 
        sign=sign, 
        form=form, 
        disorders=disorders
    )

# List of all symptoms 
@psychopathology_bp.route('/symptoms', methods=['GET'])
def show_symptoms():
    """ 
    Display a list of all symptoms.
    - Accessible only to logged-in users.
    - Includes a search form for user convenience.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    symptoms = Symptom.query.order_by(Symptom.name.asc()).all()
    form = SearchForm()

    return render_template('psychopathology/symptoms.html', symptoms=symptoms, form=form)

# Search for a symptom 
@psychopathology_bp.route('/symptoms/search', methods=['POST'])
def search_symptom():
    """
    Handle search functionality for symptoms.
    - Supports searches by ID (numeric input) or name (string input).
    - Redirects to the specific symptom's page if a match is found.
    - Displays an error message if no match is found or input is invalid.
    """

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        # Search by ID or name
        if search_query.isdigit():
            symptom = Symptom.query.filter_by(id=int(search_query)).first()
        else:
            symptom = Symptom.query.filter(Symptom.name.ilike(f"%{search_query}%")).first()
        
        # If there's a match for symptom, redirect to symptom's page
        if symptom:
            return redirect(url_for('psychopathology.get_symptom', symptom_id=symptom.id))
        
    flash("Please enter a valid search query.", "danger")
    return redirect(url_for('psychopathology.show_symptoms'))

# Autocomplete suggestions for symptom search
@psychopathology_bp.route('/symptoms/autocomplete', methods=['GET'])
def autocomplete_symptom():
    """
    Provide a JSON list of symptom names matching the user's input.
    - Matches are case-insensitive.
    - Returns an empty list if no input is provided or no matches are found.
    """    

    query = request.args.get('query', '').strip()
    print(f"Received query: {query}")  # Debugging log

    if not query:
        return jsonify([])

    # Perform a case-insensitive match
    matching_symptoms = Symptom.query.filter(Symptom.name.ilike(f"{query}%")).all()
    # Return only the names of the symptoms
    symptom_names = [symptom.name for symptom in matching_symptoms]

    return jsonify(symptom_names)

# Symptom details
@psychopathology_bp.route('/symptoms/<int:symptom_id>',  methods=['GET'])
def get_symptom(symptom_id):
    """
    Display details of a specific symptom.
    - Includes the symptom's description, associated examples, 
      and related disorders with this symptom.
    - Accessible only to logged-in users.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    symptom = Symptom.query.get_or_404(symptom_id)
    form = SearchForm()

    # Retrieve disorders associated with this symptom 
    disorders = (
        Disorder.query
        .join(DisorderSymptom, Disorder.id == DisorderSymptom.disorder_id)
        .filter(DisorderSymptom.symptom_id == symptom.id).all()
    )

    return render_template(
        'psychopathology/symptom.html', 
        symptom=symptom, 
        form=form, 
        disorders=disorders)






