from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
# from flask_login import login_required 
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User, Sign, SignExample, Disorder, DisorderSign, Symptom, SymptomExample, DisorderSymptom
from src.application.forms import SearchForm
# from src.application.forms import 

psychopathology_bp = Blueprint('psychopathology', __name__, template_folder='templates/psychopathology')

#############################################################################
# PSYCHOPATHOLOGY ITEMS (Present in the DSM-5-TR)

# All signs route
@psychopathology_bp.route('/signs', methods=['GET'])
def show_signs():
    """Show all signs."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    signs = Sign.query.all()
    form = SearchForm()

    return render_template('psychopathology/signs.html', signs=signs, form=form)

# Search sign to use in the sings page
# SHOULDN'T THIS BE A 'GET' REQUEST!!!!!! CHECK THIS OUT WHEN I HAVE THE DATA IN THE DB
@psychopathology_bp.route('/signs/search', methods=['POST'])
def search_sign():
    """Handle the search form submission for signs within the psychopathology blueprint."""
    
    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        # Check if the input is a number (for ID search)
        if search_query.isdigit():
            sign = Sign.query.filter_by(id=int(search_query)).first()
        else:
            # Otherwise search by name
            sign = Sign.query.filter(Sign.name.ilike(f"%{search_query}%")).first()
        
        # If there is a match for sign, redirect to the sign's page
        if sign:
            return redirect(url_for('psychopathology.get_sign', sign_id=sign.id))
        
        # Flash message if form validation fails
        flash('Please enter a valid term', 'dange')
        return redirect(url_for('psychopathology.show_signs'))

# Autocomplete route to the search sign input
@psychopathology_bp.route('/signs/autocomplete', methods=['GET'])
def autocomplete_sign():
    """Provides a JSON list of sign names matchin the user's input query."""

    query = request.args.get('query', '').strip()

    # If no query provided, return empty list
    if not query:
        return jsonify([])
    
    # Perform a case-insensitive match
    matching_signs = Sign.query.filter(Sign.name.ilike(f"{query}%")).all()

    # Return only the names of the signs
    sign_names = [sign.name for sign in matching_signs]

    return jsonify(sign_names)

# Sign route
@psychopathology_bp.route('/signs/<int:sign_id>', methods=['GET'])
def get_sign(sign_id):
    """
    Retrieve a sign along with:
    - Description of the sign
    - Examples of the sign
    - Search form for a sign
    - Syndromes (disorders) that have this sign
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    # Retrieve the sign and related data
    sign = Sign.query.get_or_404(sign_id)
    # sign_examples = SignExample.query.filter_by(sign_id=sign.id).all()

    form = SearchForm()

    # Retrieve disorders associated with this sign through the DisorderSign table
    disorders = (
        Disorder.query
        .join(DisorderSign, Disorder.id == DisorderSign.disorder_id)
        .filter(DisorderSign.sign_id == sign.id)
        .all()
    )

    return render_template(
        'psychopathology/sign.html', 
        sign=sign, 
        # sign_examples=sign_examples,  
        form=form, 
        disorders=disorders
    )

# All symptoms route
@psychopathology_bp.route('/symptoms', methods=['GET'])
def show_symptoms():
    """Show all symptoms."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    symptoms = Symptom.query.all()
    form = SearchForm()

    return render_template('psychopathology/symptoms.html', symptoms=symptoms, form=form)

# Search symptom function to use in the signs page
@psychopathology_bp.route('/symptoms/search', methods=['POST'])
def search_symptom():
    """Handle the search form submission for symptom within the psychopathology blueprint."""

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        # Check if the input is a number (for ID search)
        if search_query.isdigit():
            symptom = Symptom.query.filter_by(id=int(search_query)).first()
        else:
            # Otherwise search by name
            symptom = Symptom.query.filter(Symptom.name.ilike(f"%{search_query}%")).first()
        
        # If there's a match for symptom, redirect to symptom's page
        if symptom:
            return redirect(url_for('psychopathology.get_symptom', symptom_id=symptom.id))
        
 
    # Flash message if form validation fails
    flash("Please enter a valid search query.", "danger")
    return redirect(url_for('psychopathology.show_symptoms'))

# Autocomplete route to the search symptom input
@psychopathology_bp.route('/symptoms/autocomplete', methods=['GET'])
def autocomplete_symptom():
    """Provides a JSON list of symptom names matching the user's input query."""    

    query = request.args.get('query', '').strip()
    print(f"Received query: {query}")  # Debugging log

    # If no query provided, return an empty list
    if not query:
        return jsonify([])

    # Perform a case-insensitive match
    matching_symptoms = Symptom.query.filter(Symptom.name.ilike(f"{query}%")).all()
    print(f"Matching symptoms: {matching_symptoms}")  # Debugging log

    # Return only the names of the symptoms
    symptom_names = [symptom.name for symptom in matching_symptoms]
    print(f"Symptom names: {symptom_names}")  # Debugging log

    return jsonify(symptom_names)



# Symptom route
@psychopathology_bp.route('/symptoms/<int:symptom_id>',  methods=['GET'])
def get_symptom(symptom_id):
    """Retrieve a symptom along with:
    - Description of the symptom
    - Examples of the symptom
    - Search form for a symptom
    - Syndromes (disorders) that have this symptom.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    # Retrieve the symptom and related data
    symptom = Symptom.query.get_or_404(symptom_id)
    # symptom_examples = SymptomExample.query.filter_by(symptom_id=symptom.id).all()
    form = SearchForm()

    # Retrieve disorders associated with this symptom through the DisorderSymptom table
    disorders = (
        Disorder.query
        .join(DisorderSymptom, Disorder.id == DisorderSymptom.disorder_id)
        .filter(DisorderSymptom.symptom_id == symptom.id).all()
    )

    return render_template(
        'psychopathology/symptom.html', 
        symptom=symptom, 
        # symptom_examples=symptom_examples, 
        form=form, 
        disorders=disorders)






