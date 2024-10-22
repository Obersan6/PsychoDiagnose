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

# ROUTES

SEE IF I CAN REMOVE ANY ROUTES!!!!!!!! AND IF THE PATH OF EACH ROUTE IS WELL DEFINED!!!!!!!!

SEE IF I SHOULD CREATE SEPARATE FILES PER TYPE OF ROUTE AND HOW TO DO IT.

# Homepage
@app.route('/home')
def homepage():
    """Home page."""

# User Routes

# Signup route
@app.route('/signup')
def signup():

# Signin route
@app.route('/signin')
def signin():

# User profile route
@app.route('/user/<int:user_id>')
def user_profile(user_id):

# Edit route
@app.route('/user/<int:user_id>/edit')
def edit_user_profile(user_id):

# Delete user page
@app.route('/user/<int:user_id>/delete')
def delete_user_profile(user_id):

# DSM-5-TR ROUTES

# DSM route
@app.route('/dsm')
def dsm():

# List of categories route
@app.route('/categories')
def show_categories():

# Category route
@app.route('/categories/<int"category_id>')
def show_categories(category_id):

# List of disorders route
@app.route('categories/disorders')
def show_disorders():

# Disorder route
@app.route('/categories/disorders/<int:disorder_id')
def show_disorders(disorder_id):

# For those categories that have sub-groups of disorders
@app.route('/categories/clusters')
def show_clusters():

# Cluster route
@app.route('/categories/clusters/<id:cluster_id>')
def clusters(cluster_id):

# List of steps route
@app.route('/steps')
def show_steps():

# Step route
@app.route('/steps/<int:step_id>')
def step(step_id):

# Differential diagnosis route
@app.route('/diagnosis/differential_diagnosis')
def differential_diagnosis();
    
# PSYCHOPATHOLOGY ITEMS (Present in the DSM-5-TR)

# Sign route
@app.route('/signs/<int:sign_id>')
def sign(sign_id):

# Sign example route
@app.route('/signs/<int:sign_id>/example')
def sign_example(sign_id):

# Symptom route
@app.route('/symptom/<int:symptom_id>')
def symptom(symptom_id):

# Symptom example route
@app.route('/symptom/<int:symptom_id>/example')
def symptom_example(symptom_id):
















