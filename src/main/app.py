"""Flask app for dsm-diagnosis tool."""

from flask import Flask, g, session
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import LoginManager # More secured way to handle user authentication without manually checking on each route (g.user)
from src.application.models import db, connect_db, User, Category, Disorder, Cluster, Step, DifferentialDiagnosis, Sign, SignExample, Symptom, SymptomExample, DisorderSign, DisorderSymptom  
from src.application.secret_keys import SECRET_KEY, SQLALCHEMY_DATABASE_URI  # Import both vars from secret_keys.py
from src.config import DevelopmentConfig, ProductionConfig, CURR_USER_KEY
import os

# Initialize the app
# app = Flask(__name__)
app = Flask(__name__, static_folder='../application/static')

# Load configuration based on environment
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Set the secret key and database URI from the secret_keys.py file
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Initialize CSRF Protection
csrf = CSRFProtect(app)

# Initialize extensions
debug = DebugToolbarExtension(app)
connect_db(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# # Initialize LoginManager
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'user.signin'  # Redirect to the 'signin' route in user_bp for login

# # Define the user loader function
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# Import and register Blueprints
from src.application.blueprints.homepage.routes import homepage_bp
from src.application.blueprints.user.routes import user_bp
from src.application.blueprints.dsm.routes import dsm_bp
from src.application.blueprints.psychopathology.routes import psychopathology_bp

app.register_blueprint(homepage_bp)
app.register_blueprint(user_bp)
app.register_blueprint(dsm_bp)
app.register_blueprint(psychopathology_bp)

# Create database tables (if needed)
with app.app_context():
    db.create_all()

@app.before_request
def add_user_to_g():
    """Set g.user and g.logged_in before each request."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        g.logged_in = True
    else:
        g.user = None
        g.logged_in = False






















