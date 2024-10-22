"""Flask app for dsm-diagnosis tool."""

import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from src.secret_keys import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask_debugtoolbar import DebugToolbarExtension
from src.models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

debug = DebugToolbarExtension(app)

connect_db(app)

#############################################################################
# ROUTES



# SEE IF I WANT TO CREATE A BLUEPRINT STRUCTURE (different files for groups of routes)FOR THE CAPSTONE OR SHOULD I LEAVE THIS FOR LATER OR FOR ENHANCEMENTS

# Homepage 
@app.route('/home', methods=['GET'])
def homepage():
    """Home page."""

#############################################################################
# User Routes

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():

# Signin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():

# Signout route
@app.route('user/<int:user_id>/logout', methods=['POST'])
def logout(user_id):

# User profile and update user profile route 
@app.route('/user/<int:user_id>/profile', methods=['GET', 'PATCH']) 
def user_profile(user_id):

# Delete user page
@app.route('/user/<int:user_id>/profile', methods=['DELETE']) 
def delete_user_profile(user_id):

#############################################################################
# DSM-5-TR ROUTES

# DSM route
@app.route('/dsm', methods=['GET'])
def dsm():

# List of categories route 
@app.route('/categories', methods=['GET'])
def show_categories():

# Category route
@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):

# List of disorders route 
@app.route('/categories/<int:category_id>/disorders', methods=['GET'])
def show_disorders(category_id):

# Disorder route
@app.route('/categories/<int:category_id>/disorders/<int:disorder_id>', methods=['GET'])
def get_disorder(category_id, disorder_id):

# For those categories that have sub-groups of disorders 
@app.route('/categories/<int:category_id>/clusters', methods=['GET'])
def show_clusters(category_id):

# Cluster route
@app.route('/categories/<int:category_id>/clusters/<int:cluster_id>', methods=['GET']) 
def get_cluster(category_id, cluster_id):

# List of steps route 
@app.route('/steps', methods=['GET'])
def show_steps():

# Step route
@app.route('/steps/<int:step_id>', methods=['GET'])
def get_step(step_id):

# Differential diagnosis route
@app.route('/disorder/<int:disorder_id>/differential_diagnosis', methods=['GET'])
def get_differential_diagnosis(disorder_id):

#############################################################################
# PSYCHOPATHOLOGY ITEMS (Present in the DSM-5-TR)

# Sign route
@app.route('/signs/<int:sign_id>',  methods=['GET'])
def get_sign(sign_id):

# Sign example route
@app.route('/signs/<int:sign_id>/example',  methods=['GET'])
def get_sign_example(sign_id):

# Symptom route
@app.route('/symptoms/<int:symptom_id>',  methods=['GET'])
def get_symptom(symptom_id):

# Symptom example route
@app.route('/symptoms/<int:symptom_id>/example',  methods=['GET'])
def get_symptom_example(symptom_id):
















