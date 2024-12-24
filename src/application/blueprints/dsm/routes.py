from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, g, session
from sqlalchemy.exc import IntegrityError
from src.config import CURR_USER_KEY
from src.application.models import db, connect_db, User, Category, Cluster, Disorder, Sign, Symptom, DifferentialDiagnosis, Step
from src.application.forms import StepForm, SearchForm

#  Blueprint for DSM-related routes

dsm_bp = Blueprint('dsm', __name__, template_folder='templates/dsm') 

#############################################################################
# DSM-5-TR ROUTES

# DSM  overview route
@dsm_bp.route('/dsm', methods=['GET'])
def dsm():
    """
    Provides an introduction to the DSM-5-TR:
    - Its purpose
    - Sections it includes
    - General usage
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    else:
        return render_template('dsm/dsm.html')

# List of diagnostic categories 
@dsm_bp.route('/categories', methods=['GET'])
def show_categories():
    """Displays all diagnostic categories in the DSM-5-TR."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    else: 
        # categories = Category.query.all() 
        categories = Category.query.order_by(Category.name.asc()).all()
        form = SearchForm()

        return render_template('dsm/categories.html', categories=categories, form=form)

#  Search for a diagnostic category
@dsm_bp.route('/categories/search', methods=['GET', 'POST'])
def search_category():
    """
    Handles category search functionality:
    - Allows users to search categories by name or ID.
    - Redirects to the matching category's detail page, if found.
    """

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

    if search_query.isdigit():
        category = Category.query.filter_by(id=int(search_query)).first()
    else:
        category = Category.query.filter(Category.name.ilike(f"%{search_query}%")).first()
    
    if category:
        return redirect(url_for('dsm.get_category', category_id=category.id))
    else:
        flash('No category found matching that query', 'danger')
    
    flash('Please enter a valid search term', 'danger')
    return redirect(url_for('dsm.show_categories'))

# Autocomplete suggestions for category search
@dsm_bp.route('/categories/autocomplete', methods=['GET'])
def autocomplete_categories():
    """
    Provides autocomplete suggestions for category names.
    Returns a JSON list of matching category names.
    """
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([]) 

    matching_categories = Category.query.filter(Category.name.ilike(f"{query}%")).all()
    category_names = [category.name for category in matching_categories]
    
    return jsonify(category_names)

# Diagnostic category details
@dsm_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Displays detailed information for a diagnostic category:
    - Category name and description
    - Associated clusters (if any)
    - List of disorders within the category
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    category = Category.query.get_or_404(category_id)
    clusters = Cluster.query.filter_by(category_id=category_id).all()
    disorders = Disorder.query.filter_by(category_id=category_id).all()
    
    return render_template('dsm/category.html', category=category, clusters=clusters, disorders=disorders)

# List of all disorders  
@dsm_bp.route('/disorders', methods=['GET'])
# @login_required 
def show_disorders():
    """
    Displays a list of all disorders in the DSM-5-TR.
    Disorders are sorted alphabetically for easier navigation.
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    disorders = Disorder.query.order_by(Disorder.name.asc()).all()
    form = SearchForm()

    return render_template('dsm/disorders.html', disorders=disorders, form=form)

# # Search for a disorder
@dsm_bp.route('/disorders/search', methods=['GET', 'POST'])
def search_disorder():
    """
    Handles disorder search functionality:
    - Allows users to search disorders by name or ID.
    - Redirects to the matching disorder's detail page, if found.
    """

    form = SearchForm()
    if form.validate_on_submit():
        search_query = form.search_query.data.strip()

        if search_query.isdigit():
            disorder = Disorder.query.filter_by(id=int(search_query)).first()
        else:
            disorder = Disorder.query.filter(Disorder.name.ilike(f"%{search_query}%")).first()
        
        if disorder:
            return redirect(url_for('dsm.get_disorder', disorder_id=disorder.id))
        else:
            flash('No disorder found matching that query', 'danger')
        
        flash('Please enter a valid search term', 'danger')
        return redirect(url_for('dsm.show_disorders'))

# Autocomplete suggestions for disorder search
@dsm_bp.route('/disorders/autocomplete', methods=['GET'])
def autocomplete_disorders():
    """
     Provides autocomplete suggestions for disorder names.
    Returns a JSON list of matching disorder names.
    """

    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])
    
    matching_disorders = Disorder.query.filter(Disorder.name.ilike(f"{query}%")).all()
    disorder_names = [disorder.name for disorder in matching_disorders]

    return jsonify(disorder_names)   

# Disorder details
@dsm_bp.route('/disorders/<int:disorder_id>', methods=['GET'])
# @login_required 
def get_disorder(disorder_id):
    """
    Displays detailed information for a specific disorder:
    - Name, description, and diagnostic criteria
    - Associated category and cluster (if any)
    - Related signs, symptoms, and differential diagnoses
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    disorder = Disorder.query.get_or_404(disorder_id)
    category = disorder.category
    cluster = disorder.cluster
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

# List of all clusters
@dsm_bp.route('/clusters', methods=['GET'])
def show_clusters():
    """Displays a list of all cluster in the DSM-5-TR."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    clusters = Cluster.query.all()

    return render_template('dsm/clusters.html', clusters=clusters)

# Cluster details
@dsm_bp.route('/clusters/<int:cluster_id>', methods=['GET'])
def get_cluster(cluster_id):
    """
    Displays detailed information for a specific cluster
    - Name, and description
    - Associated list of disorders in the cluster
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    cluster = Cluster.query.get_or_404(cluster_id)
    disorders = Disorder.query.filter_by(cluster_id=cluster_id).all()

    return render_template('dsm/cluster.html', cluster=cluster, disorders=disorders)


# List of all steps
@dsm_bp.route('/steps', methods=['GET'])
def show_steps():
    """Shows all steps."""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))
    
    steps = Step.query.all()
    form = StepForm()

    return render_template('dsm/steps.html', steps=steps, form=form)

# Step details
@dsm_bp.route('/steps/<int:step_id>', methods=['GET'])
def get_step(step_id):
    """Displays detailed information for a specific step"""

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    step = Step.query.get_or_404(step_id)
    next_step = Step.query.filter(Step.id > step.id).order_by(Step.id.asc()).first()
    previous_step = Step.query.filter(Step.id < step.id).order_by(Step.id.desc()).first()

    return render_template(
        'dsm/step.html',
        step=step,
        next_step=next_step,
        previous_step=previous_step,
    )

# Differential diagnosis explanation
@dsm_bp.route('/differential_diagnosis', methods=['GET'])
# @login_required 
def differential_diagnosis():
    """
    Displays an explanation of differential diagnosis:
    - What it is
    - Its importance in clinical and academic settings
    """

    if not g.user:
        flash('Unauthorized. Please login', 'danger')
        return redirect(url_for('user.signin'))

    return render_template('dsm/diff_diagnosis.html')

