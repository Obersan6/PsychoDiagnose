from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g,session
# from flask_login import login_required 
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User, Category, Cluster, Disorder, Sign, Symptom, DifferentialDiagnosis, Step
from src.application.forms import StepForm, SearchForm

# from src.application.forms import 

dsm_bp = Blueprint('dsm', __name__, template_folder='templates/dsm') #CHECK IF I NEED TO REMOVE 'template_folder' since I didn't make subdirectories, this should be unnecessary.

#############################################################################
# DSM-5-TR ROUTES

# DSM route
@dsm_bp.route('/dsm', methods=['GET'])
def dsm():
    """Provides an introduction to what the DSM-5-TR is, what it is for, sections, and general use.

    __tablename__ = 'dsm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manual_info = db.Column(db.Text, nullable=False)
    sections = db.Column(db.Text, nullable=False)"""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    else:
        return render_template('dsm/dsm.html')

# List of Diagnostic Categories route 
@dsm_bp.route('/categories', methods=['GET'])
def show_categories():
    """
    Show all Diagnosis categories
    - Each category has several disorders.
    - Some categories have clusters (they group some disorders of the category into a sub-category.)
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    else: 
        categories = Category.query.all()
        form = SearchForm()

        return render_template('dsm/categories.html', categories=categories, form=form)

# Search category to use in the show_categories page
@dsm_bp.route('/categories/search', methods=['GET', 'POST'])
def search_category():
    """Handle the search submission for categories within the dsm blueprint."""

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

    # Check if the input is a number (for ID search)
    if search_query.isdigit():
        category = Category.query.filter_by(id=int(search_query)).first()
    else:
        # Otherwise, search by name
        category = Category.query.filter(Category.name.ilike(f"%{search_query}%")).first()
    
    if category:
        # Redirect to the specific category's page if a match is found.
        return redirect(url_for('dsm.get_category', category_id=category.id))
    else:
        # Flash message if no category is found and redirect to 'show_categories' page
        flash('No category found matching that query', 'danger')
    
    # Flash message if form validation fails
    flash('Please enter a valid search term', 'danger')
    return redirect(url_for('dsm.show_categories'))

# Autocomplete route to the search category input
@dsm_bp.route('/categories/autocomplete', methods=['GET'])
def autocomplete_categories():
    """
    Provides a JSON list of category names matching the user's input query.
    """
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])  # Return an empty list if no query provided

    # Perform a case-insensitive match
    matching_categories = Category.query.filter(Category.name.ilike(f"{query}%")).all()
    
    # Return only the names of the categories
    category_names = [category.name for category in matching_categories]
    
    return jsonify(category_names)

# Diagnostic Category route
@dsm_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Show Diagnostic Category:
    - Name of category
    - Description of category
    - List of clusters if the disorder has clusters
    - List of disorders within the category

    DON'T FORGEEEEEEEEEEEEET TO GET THE DATA FOR THIS ROUTE TO INCLUDE IN THE DATABASEEEEEEEEEEEE!!!!!!!!!!!!!
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    category = Category.query.get_or_404(category_id)
    clusters = Cluster.query.filter_by(category_id=category_id).all()
    disorders = Disorder.query.filter_by(category_id=category_id).all()
    
    return render_template('dsm/category.html', category=category, clusters=clusters, disorders=disorders)

# List of disorders route 
@dsm_bp.route('/disorders', methods=['GET'])
# @login_required 
def show_disorders():
    """Show all disorders."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    disorders = Disorder.query.all()
    form = SearchForm()

    return render_template('dsm/disorders.html', disorders=disorders, form=form)

# Search disorder to use in the show_disorders page
@dsm_bp.route('/disorders/search', methods=['GET', 'POST'])
def search_disorder():
    """Handle the search submission for search disorder within template 'disorders.html' within the dsm blueprint."""

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        # Check if the input is a number (for ID search)
        if search_query.isdigit():
            disorder = Disorder.query.filter_by(id=int(search_query)).first()
        else:
            # Otherwise, search by name
            disorder = Disorder.query.filter(Disorder.name.ilike(f"%{search_query}%")).first()
        
        # If there's a match for disorder, redirect to disorder's page
        if disorder:
            return redirect(url_for('dsm.get_disorder', disorder_id=disorder.id))
        else:
            # Flash message if no category is found and redirect to show_categories page
            flash('No disorder found matching that query', 'danger')
        
        # Flash message if form validation fails
        flash('Please enter a valid search term', 'danger')
        return redirect(url_for('dsm.show_disorders'))

# Autocomplete route to the search disorder input
@dsm_bp.route('/disorders/autocomplete', methods=['GET'])
def autocomplete_disorders():
    """Provides a JSON list of category names matchin the user's input query."""

    query = request.args.get('query', '').strip()

    # If no query provided, return an empty list
    if not query:
        return jsonify([])
    
    # Perform a case-insensitive match
    matching_disorders = Disorder.query.filter(Disorder.name.ilike(f"{query}%")).all()

    # Return only the names of the disorders
    disorder_names = [disorder.name for disorder in matching_disorders]

    return jsonify(disorder_names)   

# Disorder route
@dsm_bp.route('/disorders/<int:disorder_id>', methods=['GET'])
# @login_required 
def get_disorder(disorder_id):
    """Show Disorder:
    - Name of Disorder
    - Description of disorder
    - Criteria
    - List of signs
    - List of symptoms
    - Associated Category
    - Differential Diagnoses
    """

    # Ensure user is authenticated
    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    # Fetch the disorder or return 404 if not found
    disorder = Disorder.query.get_or_404(disorder_id)

    # Fetch associated category
    category = disorder.category

    # Only retrieve clusters if the disorder belongs to any 
    cluster = disorder.cluster
    
    # Retrieve related signs, symptoms, and differential diagnoses
    signs = disorder.disorder_signs
    symptoms = disorder.disorder_symptoms
    differential_diagnoses = DifferentialDiagnosis.query.filter_by(disorder_id=disorder.id)

    return render_template(
        'dsm/disorder.html', 
        disorder=disorder, 
        category=category, 
        cluster=cluster, 
        signs=signs, 
        symptoms=symptoms,
        differential_diagnoses=differential_diagnoses
    )

# Show all clusters
@dsm_bp.route('/clusters', methods=['GET'])
def show_clusters():
    """Show all the clusters."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    # Query clusters specific to the given category
    clusters = Cluster.query.all()

    return render_template('dsm/clusters.html', clusters=clusters)

# Cluster route
@dsm_bp.route('/clusters/<int:cluster_id>', methods=['GET'])
def get_cluster(cluster_id):
    """Show cluster:
    - Name of cluster
    - Description
    - List of disorders for the cluster.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    # Fetch the cluster, ensuring it is part of the given category
    cluster = Cluster.query.get_or_404(cluster_id)

    # Retrieve list of disorders in the cluster
    disorders = Disorder.query.filter_by(cluster_id=cluster_id).all()

    return render_template('dsm/cluster.html', cluster=cluster, disorders=disorders)


# List of steps route 
@dsm_bp.route('/steps', methods=['GET'])
def show_steps():
    """Show all steps and render the search form."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    steps = Step.query.all()
    form = StepForm()

    return render_template('dsm/steps.html', steps=steps, form=form)

# Handling searching form at route show_steps

@dsm_bp.route('/steps/search', methods=['POST'])
def search_step():
    """Handle the search form submission for a specific step."""

    form = StepForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()
        print("Search Query:", search_query)  # Debugging output

        if search_query.isdigit():
            # Search by step number
            step = Step.query.filter_by(step_number=int(search_query)).first()
            print("Step found by number:", step)  # Debugging output
        else:
            # Search by step name (case-insensitive)
            step = Step.query.filter(Step.step_name.ilike(f"%{search_query}%")).first()
            print("Step found by name:", step)  # Debugging output

        # Check if a step was found
        if step:
            print("Redirecting to get_step with step_id:", step.id)  # Debugging output
            return redirect(url_for('dsm.get_step', step_id=step.id))
        else:
            flash("No step found matching that query.", "danger")
            return redirect(url_for('dsm.show_steps'))

    flash("Please enter a valid search query.", "danger")
    return redirect(url_for('dsm.show_steps'))


# Step route
@dsm_bp.route('/steps/<int:step_id>', methods=['GET'])
def get_step(step_id):
    """Fetch and display a specific step."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    # Fetch the step
    step = Step.query.get_or_404(step_id)
    return render_template('dsm/step.html', step=step)


# Differential diagnosis route
# BECAUSE WE ALREADY GET 'DIFF. DIAGNOSIS' THE ONLY WAY IT SHOULD BE RETRIEVED WHICH IS ALONG A DISORDER (DIAGNOSIS) I'LL ONLY USE THIS ROUTE TO DISPLAY THE DESCRIPTION OF WHAT DIFF. DIAGNOSIS IS
@dsm_bp.route('/differential_diagnosis', methods=['GET'])
# @login_required 
def differential_diagnosis():
    """This route only shows an explanation of what it is and why it's important.
    At a later time, this route may be modified."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    return render_template('dsm/diff_diagnosis.html')


# # THIS COULD BE A ROUTE FOR LATER, FOR THE TIME BEING IS REDUNDANT 
# @dsm_bp.route('/disorder/<int:disorder_id>/differential_diagnosis', methods=['GET'])
# def get_differential_diagnosis(disorder_id):